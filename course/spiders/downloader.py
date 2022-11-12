import json
import os

import scrapy


class DownloaderSpider(scrapy.Spider):
    name = "downloader"

    def start_requests(self):
        with open("temp.json") as reader:
            data = json.loads(reader.read())

        for doc in data:
            link = doc["details"]["video_mp4_link"]

            # directory = source.replace("https://campus.datacamp.com/courses/", "").split("/")
            # folder_name = directory[0]
            # file_name_items = directory[1].split("?")
            # file_name = file_name_items[1].replace("=", "-") + " - " + file_name_items[0]

            folder_name = doc["course_name"]
            file_name = doc["chapter_name"]

            if not os.path.isdir(f"data/videos/{folder_name}"):
                os.mkdir(f"data/videos/{folder_name}")

            yield scrapy.Request(
                url=link,
                headers={
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ar-AE;q=0.6,ar;q=0.5,bn-BD;q=0.4,bn;q=0.3",
                    "Origin": "https://projector.datacamp.com",
                    "Referer": "https://projector.datacamp.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "cross-site",
                    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24""',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                },
                callback=self.parse,
                cb_kwargs={"folder_name": folder_name, "file_name": file_name},
            )

    def parse(self, response, **kwargs):
        folder_name = kwargs["folder_name"]
        file_name = kwargs["file_name"]
        data = response.body
        with open(f"data/videos/{folder_name}/{file_name}.mp4", "wb") as writer:
            writer.write(data)
