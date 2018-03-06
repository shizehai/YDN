#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from pymongo import MongoClient
from bs4 import BeautifulSoup
import logging
import os,datetime,time
import lxml.etree
from lxml.etree import *
import json,codecs,re,copy
from selenium import webdriver
import requests,urllib
from settings import MONGODB_IP,MONGODB_DB,MONGODB_TABLE

# 导入 items 下面的自定义 Item 类
from CarComment.items import Item

# try:
#   from map.items import mapItem
# except Exception as e:
#     print e


class cc_autohome(scrapy.Spider):

    name = 'cc_autohome' # 必须, 对应的使用 scrapy crawl <name> 指令运行爬虫
    
    def start_requests(self):
        with open('keywords.csv') as fr:
            keywords = fr.readlines()
        page = 1
        for keyword in keywords:
            keyword=keyword.replace('\n','')
            url_='www.example.com/{keyword}/{page}'
            url = url_.format(keyword=keyword, page=str(page))
            item = Item()
            item['keyword'] = keyword
            req = scrapy.Request(url, callback=self.parse_list_item)
            req.meta['page'] = page
            req.meta['item'] = copy.deepcopy(item)
            req.meta['url_'] = copy.deepcopy(url_)
            yield req
        
    def parse_list_item(self, response):
        item = copy.deepcopy(response.meta['item'])
        page = response.meta['page']
        keyword=item['keyword']
        last_url_=response.meta['url_']
        
        # response文本预处理
        soup = BeautifulSoup(response.text)
        lines = soup.find(class_="result").find_all(class_="list-dl")

        count = len(lines)
        # 翻页
        
        if int(page) < 10 or int(count) < 10:
            page=str(int(page+1))
            last_url=last_url_.format(keyword=keyword, page=str(page))
            req = scrapy.Request(last_url, callback=self.parse_list_item)
            req.meta['item'] = copy.deepcopy(item)
            req.meta['page'] = page
            req.meta['url_'] = copy.deepcopy(last_url_)
            req.meta['keyword']=keyword
            
            yield req
    
        items = []
        for line in lines:
            page=1
            # 解析 item 数据
            title=line.find(class_='').find(class_='')
            site_url=line.find(class_='').find(class_='')
            site_name=line.find(class_='').find(class_='')
            group=line.find(class_='').find(class_='')
            rel_time=line.find(class_='').find(class_='')
            
            item['title']=title
            item['site_url']=site_url
            item['site_name']=site_name
            item['group']=group
            item['rel_time']=rel_time
            
            
        
            formdata={}
            url=url_
            req = scrapy.FormRequest(url,formdata=formdata, callback=self.parse_item)
            req.meta['item'] = copy.deepcopy(item)
            req.meta['page'] = page
            req.meta['url_'] = copy.deepcopy(url_)
            
            yield req
    

    def parse_item(self, response):
        item = copy.deepcopy(response.meta['item'])
        page = response.meta['page']
        keyword=item['keyword']
        last_url_=response.meta['url_']
        keyword=response.meta['keyword']
        
        # response文本预处理
        soup = BeautifulSoup(response.text)
        lines = soup.find(class_="result").find_all(class_="list-dl")

        count = len(lines)
        # 翻页
        
        if int(page) < 10 or int(count) < 10:
            page=str(int(page+1))
            last_url=last_url_.format(keyword=keyword, page=str(page))
            req = scrapy.Request(last_url, callback=self.parse_item)
            req.meta['item'] = copy.deepcopy(item)
            req.meta['page'] = page
            req.meta['url_'] = copy.deepcopy(last_url_)
            req.meta['keyword']=keyword
            
            yield req
    
        items = []
        for line in lines:
            page=1
            # 解析 item 数据
            content=line.find(class_='').find(class_='')
            
            item['content']=content
        
            items=items.append(item)
        req=scrapy.Request('https://www.baidu.com',callback=self.tomongodb)
        req.meta['items']=items
    def tomongodb(self,response):
        items=response.meta['items']
        # 写入数据库，通用
        if items <> []:
            def pre_process_item(item):
                for key, value in item.iteritems():
                    if isinstance(value, str) or isinstance(value, unicode):
                        item[key] = value.replace('\t', '').replace('\r', '').replace('\n', '').strip()
            items = map(pre_process_item, items)
            # 修改数据库名、数据表名
            client = MongoClient(MONGODB_IP, 27017)
            # 修改数据库名、数据表名
            db = client[MONGODB_DB]
            db_key = db[MONGODB_TABLE]
            info = db_key.insert_many(items)
