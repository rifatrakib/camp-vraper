import json
import scrapy


class CourseCatalogueSpider(scrapy.Spider):
    name = "course_catalogue"
    start_urls = ["https://learn-hub-api.datacamp.com/courses?first=12&sort=&&&"]
    
    def read_headers(self):
        with open("course/static/headers.json") as reader:
            self.headers = json.loads(reader.read())
    
    def read_cookies(self):
        with open("course/static/cookies.json") as reader:
            self.cookies = json.loads(reader.read())
    
    def start_requests(self):
        url = self.start_urls[0]
        self.read_headers()
        self.read_cookies()
        yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        data = response.json()
        end_cursor = data.get("endCursor", None)
        
        for course in data.get("items"):
            yield course
        
        if end_cursor:
            url = self.start_urls[0] + f"&after={end_cursor}"
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)
