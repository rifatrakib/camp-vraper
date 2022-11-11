import json
import subprocess

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

command = "scrapy crawl downloader"
subprocess.run(command, shell=True)
