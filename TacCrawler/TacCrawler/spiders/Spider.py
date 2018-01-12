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
import json,codecs,re
import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests,urllib
# 导入 items 下面的自定义 Item 类
from TacCrawler.items import Item
# try:
#   from map.items import mapItem
# except Exception as e:
#     print e

class TAC(scrapy.Spider):
    name = 'numberingplans' # 必须, 对应的使用 scrapy crawl <name> 指令运行爬虫
    #

    def start_requests(self):
        head_nums=['49','44','35','33','52','50',]
        page='1'
        for head_num in head_nums:
            url = 'https://www.numberingplans.com/?page=plans&sub=imeinr&' \
                       'alpha_2_input={head_num}&current_page={page}'.format(head_num=head_num, page=page)
            req=scrapy.Request(url,callback=self.parse)
            req.meta['head_num']=head_num
            req.meta['page'] = page
            yield req
    def parse(self,response):
        head_num=response.meta['head_num']
        page=response.meta['page']
        soup = BeautifulSoup(response.text,'lxml')
        table = soup.find_all('table', id="AutoNumber1")[1]
        rows = table.find_all('tr')

        count=len(rows[2:-1])
        if count==10:
            page=str(int(page)+1)
            url = 'https://www.numberingplans.com/?page=plans&sub=imeinr&' \
                  'alpha_2_input={head_num}&current_page={page}'.format(head_num=head_num, page=page)
            req = scrapy.Request(url, callback=self.parse)
            req.meta['head_num'] = head_num
            req.meta['page'] = page
            yield req
        for row in rows[2:-1]:
            if row:
                cols = row.find_all('td')
                TAC = cols[0].get_text().strip()
                manufacturer = cols[1].get_text().strip()
                brand_model = cols[2].get_text().strip()
                item = Item()
                date_str = datetime.datetime.now().strftime('%Y-%m-%d')
                item['date'] = date_str
                item['spider_name'] = self.name
                item['host'] = 'numberingplans.com'
                item['head_num'] = head_num
                item['TAC'] = TAC
                item['manufacturer'] = manufacturer
                item['brand_model'] = brand_model
                yield item

