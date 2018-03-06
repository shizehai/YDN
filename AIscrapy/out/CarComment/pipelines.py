# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import datetime
from settings import MONGODB_IP,MONGODB_DB,MONGODB_TABLE
from pymongo import MongoClient
class PreprocessPipeline(object):
    def process_item(self, item, spider):
        for key,value in item.iteritems():
            if isinstance(value, str) or isinstance(value, unicode):
                item[key] = value.replace('\t', '').replace('\r', '').replace('\n', '').strip()
        return item
class toCsvPipeline(object):
    def process_item(self, item, spider):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')

        with codecs.open('OUT_' +spider.name+'_'+ date_str + '.csv', 'a+', encoding='utf-8') as fout:
            fout.write('\t'.join(dict(item).values()) + '\n')
        return item

class toMongodbPipeline(object):
    def process_item(self, item, spider):


        if item:
            client = MongoClient(MONGODB_IP, 27017)
            # 修改数据库名、数据表名
            db = client[MONGODB_DB]
            db_key = db[MONGODB_TABLE]
            info = db_key.insert_many(item)
        return item
