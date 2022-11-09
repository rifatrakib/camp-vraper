import json

import pymongo
from itemadapter import ItemAdapter
from scrapy import signals


class CoursePipeline:
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        spider_name = spider.name.replace("_", "-")
        self.file = open(f"data/{spider_name}.json", "w")
        header = "[\n"
        self.file.write(header)

    def spider_closed(self, spider):
        footer = "]\n"
        self.file.write(footer)
        self.file.close()

        spider_name = spider.name.replace("_", "-")
        with open(f"data/{spider_name}.json", "r") as reader:
            data = reader.read()

        data = data.rpartition(",")
        data = data[0] + data[-1]
        with open(f"data/{spider_name}.json", "w") as writer:
            writer.write(data)

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), indent=4) + ",\n"
        self.file.write(line)
        return item


class MongoPipeline:
    collection_name = "courses"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
