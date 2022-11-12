import json
import subprocess

from dotenv import load_dotenv

from course.utils import MongoConnectionManager

load_dotenv()


def build_cookie_data(cookie_string):
    cookies = {}
    for cookie in cookie_string.split("; "):
        key, value = cookie.split("=", 1)
        cookies[key] = value

    return cookies


def build_header_data(header_string):
    headers = {}
    for header in header_string.split("|"):
        key, value = header.split("=", 1)
        headers[key] = value

    return headers


def update_scraped_json(spider_name, update=True):
    with open(f"data/{spider_name}-catalogue.json") as reader:
        data = json.loads(reader.read())

    if update:
        with open(f"data/scraped-data/{spider_name}-catalogue.json", "r") as reader:
            old_data = json.loads(reader.read())
        data = old_data + data

    with open(f"data/scraped-data/{spider_name}-catalogue.json", "w") as writer:
        writer.write(json.dumps(data))


def preprocess_downloader_data():
    with open("data/video-catalogue.json") as reader:
        data = json.loads(reader.read())

    records = []
    parents = []
    for doc in data:
        if "video_mp4_link" in doc:
            records.append(doc)
        else:
            parents.append(doc)

    results = []
    for doc in parents:
        for record in records:
            if doc["video_url"] == record["page_url"]:
                doc["details"] = record
                results.append(doc)
                break

    with open("temp.json", "w") as writer:
        writer.write(json.dumps(results, indent=4))


def run_spider(spider_name):
    command = f"scrapy crawl {spider_name}_catalogue 2>&1 | tee {spider_name}-crawl.log"
    subprocess.run(command, shell=True)


headers = ["course", "chapter", "video", "player", "transcript", "download"]
for header in headers:
    with open(f"course/static/{header}-catalogue/headers.json", "w") as writer:
        with open(f"course/static/{header}-catalogue/headers.txt") as reader:
            data = build_header_data(reader.read())
        writer.write(json.dumps(data, indent=4))

    if header not in {"transcript", "download"}:
        with open(f"course/static/{header}-catalogue/cookies.json", "w") as writer:
            with open(f"course/static/{header}-catalogue/cookies.txt") as reader:
                data = build_cookie_data(reader.read())
            writer.write(json.dumps(data, indent=4))


run_spider("course")
update_scraped_json("course", update=False)
run_spider("chapter")
update_scraped_json("chapter", update=False)

collection_name = "chapters"
with MongoConnectionManager(collection_name) as session:
    data = list(session.find({}, {"_id": 0, "chapters": 1, "slug": 1}))

with open("chapters.json", "w") as writer:
    writer.write(json.dumps(data, indent=4))

while True:
    with open("chapters.json") as reader:
        if not json.loads(reader.read()):
            print("all chapters from all courses have been scraped")
            break

    run_spider("video")
    update_scraped_json("video")
    preprocess_downloader_data()
    run_spider("downloader")
