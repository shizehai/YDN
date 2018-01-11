# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import datetime
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
        data_list = []
        data_dic = dict(item)
        data_list.insert(0, data_dic['date'])
        data_list.insert(1, data_dic['spider_name'])
        data_list.insert(2, data_dic['map_type'])
        data_list.insert(3, str(data_dic['tag_id']))
        data_list.insert(4, data_dic['tag_name'])
        data_list.insert(5, data_dic['res_tag_name'])
        data_list.insert(6, data_dic['LonLat'])

        with codecs.open(item['spider_name'] + '_' + date_str + '.csv', 'a+', encoding='utf-8') as fout:
            fout.write('\t'.join(data_list) + '\n')
        return item

class toMongodbPipeline(object):
    def process_item(self, item, spider):
        if item:
            client = MongoClient('192.168.11.17', 27017)
            # 修改数据库名、数据表名
            db = client['CrawlerData_other']
            db_key = db['Mobile_tac']
            info = db_key.insert(dict(item))
        return item
