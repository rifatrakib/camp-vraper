import json

import scrapy

from course.items import VideoAdditives, VideoInformation


class VideoCatalogueSpider(scrapy.Spider):
    name = "video_catalogue"

    def read_headers(self):
        with open("course/static/video-catalogue/headers.json") as reader:
            self.headers = json.loads(reader.read())

    def read_player_headers(self):
        with open("course/static/player-catalogue/headers.json") as reader:
            self.player_headers = json.loads(reader.read())

    def read_downloader_headers(self):
        with open("course/static/download-catalogue/headers.json") as reader:
            self.downloader_headers = json.loads(reader.read())

    def read_cookies(self):
        with open("course/static/video-catalogue/cookies.json") as reader:
            self.cookies = json.loads(reader.read())

    def start_requests(self):
        self.read_headers()
        self.read_cookies()
        with open("chapters.json", "r") as reader:
            data = json.loads(reader.read())

        course_to_scrape = data[0]
        course_name = course_to_scrape["slug"]
        chapters = course_to_scrape["chapters"]

        # with MongoConnectionManager("videos") as session:
        #     exclude = list(session.find({"visited": True}, {"_id": 0, "video_url": 1}))

        # urls = [chapter["link"] for doc in data for chapter in doc["chapters"]]
        # exclude = [doc["video_url"] for doc in exclude]
        # urls = list(set(urls) - set(exclude))
        # for url in urls:
        for index, chapter in enumerate(chapters):
            yield scrapy.Request(
                # url=url,
                url=chapter["link"],
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse,
                cb_kwargs={
                    "chapter_name": f"{index + 1} - {chapter['title']}".replace("?", "").replace("/", "-"),
                    "course_name": course_name.replace("?", "").replace("/", "-"),
                },
            )

        with open("chapters.json", "w") as writer:
            writer.write(json.dumps(data[1:], indent=4))

    def parse(self, response, **kwargs):
        video_api = "https://projector.datacamp.com/?auto_play=play"
        transcript_api = "https://projector.datacamp.com/api/videos"
        page_url = response.request.url
        response = response.css('script[type="application/ld+json"]::text').get()
        data = {}
        for key, value in json.loads(response).items():
            data[key if key[0] != "@" else key[1:]] = value

        data["course_name"] = kwargs["course_name"]
        data["chapter_name"] = kwargs["chapter_name"]
        data["page_url"] = page_url
        data["projector_key"] = data["embedUrl"].split("?projector_key=")[-1]
        data["video_url"] = f"{video_api}&projector_key={data['projector_key']}"
        data["transcript_url"] = f"{transcript_api}/{data['projector_key']}/transcript"

        self.read_player_headers()
        yield scrapy.Request(
            url=data["video_url"],
            headers=self.player_headers,
            callback=self.parse_video_link,
            cb_kwargs={"source": data["page_url"]},
        )

        yield VideoInformation(**data)

    def parse_video_link(self, response, **kwargs):
        data = response.css('input#videoData::attr("value")').get()
        data = json.loads(data)
        data["page_url"] = response.request.url
        # source = kwargs["source"]

        # directory = source.replace("https://campus.datacamp.com/courses/", "").split("/")
        # folder_name = directory[0]
        # file_name_items = directory[1].split("?")
        # file_name = file_name_items[1].replace("=", "-") + " - " + file_name_items[0]

        # if not os.path.isdir(f"data/{folder_name}"):
        #     os.mkdir(f"data/{folder_name}")

        # self.download_video(data["video_mp4_link"], folder_name, file_name)
        print(data["page_url"])
        yield VideoAdditives(**data)

    # def download_video(self, url, folder_name, file_name):
    #     self.read_downloader_headers()
    #     headers = self.downloader_headers
    # response = requests.get(url, headers=headers)
    # with open(f"data/{folder_name}/{file_name}.mp4", "wb") as writer:
    #     writer.write(response.content)
