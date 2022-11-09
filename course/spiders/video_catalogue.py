import json

import scrapy

from course.items import VideoInformation
from course.utils import MongoConnectionManager


class VideoCatalogueSpider(scrapy.Spider):
    name = "video_catalogue"

    def read_headers(self):
        with open("course/static/video-catalogue/headers.json") as reader:
            self.headers = json.loads(reader.read())

    def read_cookies(self):
        with open("course/static/video-catalogue/cookies.json") as reader:
            self.cookies = json.loads(reader.read())

    def start_requests(self):
        self.read_headers()
        self.read_cookies()
        collection_name = "chapters"
        with MongoConnectionManager(collection_name) as session:
            data = list(session.find({}, {"_id": 0, "chapters": 1}))

        urls = [chapter["link"] for doc in data for chapter in doc["chapters"]]
        for url in urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse,
            )

    def parse(self, response):
        video_api = "https://projector.datacamp.com/?auto_play=play"
        transcript_api = "https://projector.datacamp.com/api/videos"
        response = response.css('script[type="application/ld+json"]::text').get()
        data = {}
        for key, value in json.loads(response).items():
            data[key if key[0] != "@" else key[1:]] = value

        data["projector_key"] = data["embedUrl"].split("?projector_key=")[-1]
        data["video_url"] = f"{video_api}&projector_key={data['projector_key']}"
        data["transcript_url"] = f"{transcript_api}/{data['projector_key']}/transcript"
        yield VideoInformation(**data)
