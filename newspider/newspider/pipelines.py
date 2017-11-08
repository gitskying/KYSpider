# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pymongo import MongoClient


class NewspiderPipeline(object):
    def open_spider(self, spider):
        client = MongoClient("127.0.0.1", 27017)
        self.collection = client["books"]["suning"]

    def process_item(self, item, spider):
        # if spider.name == 'suning':
        #     with open("../suning.txt", "a", encoding="utf-8") as f:
        #         f.write(json.dumps(dict(item), ensure_ascii=False))
        self.collection.insert(item)
        return item

    def process_item_tencent(self, item, spider):
        if spider.name == 'tencent':
            print(item)