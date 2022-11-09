import json
import subprocess

from dotenv import load_dotenv

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


spiders = ["course", "chapter", "video"]
for spider in spiders:
    with open(f"course/static/{spider}-catalogue/headers.json", "w") as writer:
        with open(f"course/static/{spider}-catalogue/headers.txt") as reader:
            data = build_header_data(reader.read())
        writer.write(json.dumps(data))

    with open(f"course/static/{spider}-catalogue/cookies.json", "w") as writer:
        with open(f"course/static/{spider}-catalogue/cookies.txt") as reader:
            data = build_cookie_data(reader.read())
        writer.write(json.dumps(data))

    command = f"scrapy crawl {spider}_catalogue"
    subprocess.run(command, shell=True)
