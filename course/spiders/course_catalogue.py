import json

import scrapy

from course.items import Course


class CourseCatalogueSpider(scrapy.Spider):
    name = "course_catalogue"
    start_urls = ["https://learn-hub-api.datacamp.com/courses?first=12&sort=&&&"]

    def read_headers(self):
        with open("course/static/course-catalogue/headers.json") as reader:
            self.headers = json.loads(reader.read())

    def read_cookies(self):
        with open("course/static/course-catalogue/cookies.json") as reader:
            self.cookies = json.loads(reader.read())

    def start_requests(self):
        url = self.start_urls[0]
        self.read_headers()
        self.read_cookies()
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            cookies=self.cookies,
            callback=self.parse,
        )

    def parse(self, response):
        data = response.json()
        end_cursor = data.get("endCursor", None)

        for course in data.get("items"):
            item_data = Course(**course)
            item_data.link = item_data.link.replace("/continue", "?embedded=true")
            yield item_data.dict()

        if end_cursor:
            url = self.start_urls[0] + f"&after={end_cursor}"
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)
