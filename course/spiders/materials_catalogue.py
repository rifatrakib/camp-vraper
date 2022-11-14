import json
import os

import scrapy


class MaterialsCatalogueSpider(scrapy.Spider):
    name = "materials_catalogue"

    def start_requests(self):
        with open("materials.json", "r") as reader:
            data = json.loads(reader.read())

        course_to_scrape = data[0]
        course_name = course_to_scrape["slug"]
        materials = course_to_scrape["materials"]

        for index, material in enumerate(materials):
            yield scrapy.Request(
                url=material["link"],
                callback=self.parse,
                cb_kwargs={
                    "material_name": f"{index + 1} - {material['title']}".replace("?", "")
                    .replace("/", "-")
                    .replace('"', "")
                    .replace(":", "- ")
                    .replace("|", "")
                    .replace("*", "-"),
                    "course_name": course_name.replace("?", "").replace("/", "-"),
                },
            )

        with open("materials.json", "w") as writer:
            writer.write(json.dumps(data[1:], indent=4))

    def parse(self, response, **kwargs):
        folder_name = kwargs["course_name"]
        file_name = kwargs["material_name"]
        location = f"data/materials/{folder_name}"

        if not os.path.isdir(location):
            os.mkdir(location)

        with open(f"{location}/{file_name}.html", "w", encoding="utf-8") as writer:
            writer.write(response.text)
