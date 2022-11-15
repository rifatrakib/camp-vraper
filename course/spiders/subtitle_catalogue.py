import json
import os

import scrapy


class SubtitleCatalogueSpider(scrapy.Spider):
    name = "subtitle_catalogue"

    def start_requests(self):
        with open("subtitles.json", "r") as reader:
            data = json.loads(reader.read())

        course_to_scrape = data[0]
        course_name = course_to_scrape["course_name"]
        chapter_name = course_to_scrape["chapter_name"]

        subtitles = []
        if course_to_scrape["details"]:
            subtitles = course_to_scrape["details"]["subtitles"]

        for subtitle in subtitles:
            yield scrapy.Request(
                url=subtitle["link"],
                callback=self.parse,
                cb_kwargs={
                    "chapter_name": chapter_name,
                    "course_name": course_name,
                    "file_name": subtitle["language"],
                },
            )

        with open("subtitles.json", "w") as writer:
            writer.write(json.dumps(data[1:], indent=4))

    def parse(self, response, **kwargs):
        file_name = kwargs["file_name"]
        course_name = kwargs["course_name"]
        chapter_name = kwargs["chapter_name"]

        location = f"data/subtitles/{course_name}"
        if not os.path.isdir(location):
            os.mkdir(location)

        location = f"{location}/{chapter_name}"
        if not os.path.isdir(location):
            os.mkdir(location)

        with open(f"{location}/{file_name}.txt", "w", encoding="utf-8") as writer:
            writer.write(response.text)
