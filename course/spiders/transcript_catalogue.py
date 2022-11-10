import json

import scrapy

from course.items import Transcript
from course.utils import MongoConnectionManager


class TranscriptCatalogueSpider(scrapy.Spider):
    name = "transcript_catalogue"

    def read_headers(self):
        with open("course/static/transcript-catalogue/headers.json") as reader:
            self.headers = json.loads(reader.read())

    def start_requests(self):
        self.read_headers()
        collection_name = "videos"
        with MongoConnectionManager(collection_name) as session:
            data = list(session.find({}, {"_id": 0, "transcript_url": 1}))

        urls = [doc["transcript_url"] for doc in data]
        for url in urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse,
            )

    def parse(self, response):
        data = response.json()
        data["url"] = response.request.url
        yield Transcript(**data)
