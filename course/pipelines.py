import json
from scrapy import signals
from itemadapter import ItemAdapter


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
