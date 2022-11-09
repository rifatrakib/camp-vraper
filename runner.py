import json
import subprocess


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
    
    return 


with open("course/static/headers.json", "w") as writer:
    with open("course/static/headers.txt") as reader:
        data = build_header_data(reader.read())
    
    writer.write(json.dumps(data))

with open("course/static/cookies.json", "w") as writer:
    with open("course/static/cookies.txt") as reader:
        data = build_cookie_data(reader.read())
    
    writer.write(json.dumps(data))

command = "scrapy crawl datacamp"
subprocess.run(command, shell=True)
