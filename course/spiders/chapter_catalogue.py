import json
import os

import scrapy

from course.items import CourseOutline, Resource
from course.utils import MongoConnectionManager


class ChapterCatalogueSpider(scrapy.Spider):
    name = "chapter_catalogue"

    def read_headers(self):
        with open("course/static/chapter-catalogue/headers.json") as reader:
            self.headers = json.loads(reader.read())

    def read_cookies(self):
        with open("course/static/chapter-catalogue/cookies.json") as reader:
            self.cookies = json.loads(reader.read())

    def start_requests(self):
        self.read_headers()
        self.read_cookies()
        collection_name = "courses"
        with MongoConnectionManager(collection_name) as session:
            data = list(session.find({}, {"_id": 0, "link": 1}))

        urls = [doc["link"] for doc in data]
        for url in urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse,
            )

    def parse(self, response):
        video_icon_url = os.environ.get("VIDEO_SVG")
        video_icon_selector = "span.chapter__exercise-icon.exercise-icon > img::attr(src)"
        url = response.request.url
        slug = url.rsplit("/", 1)[-1].replace("?embedded=true", "")

        chapters = []
        materials = []
        for root_item in response.css("ol > li > ul > li"):
            link = root_item.css("a::attr(href)").get()
            title = root_item.css("h5::text").get()
            resource = Resource(link=link, title=title)
            if root_item.css(video_icon_selector).get() == video_icon_url:
                chapters.append(resource)
            else:
                materials.append(resource)

        course_outline = CourseOutline(
            slug=slug,
            chapters=chapters,
            materials=materials,
            number_of_chapters=len(chapters),
            number_of_materials=len(materials),
        )
        yield course_outline
