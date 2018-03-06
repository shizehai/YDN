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
import json,codecs,re,copy
import requests,urllib
from $projectName$.settings import MONGODB_IP,MONGODB_DB,MONGODB_TABLE

# 导入 items 下面的自定义 Item 类
from $projectName$.items import Item

# try:
#   from map.items import mapItem
# except Exception as e:
#     print e


class $spiderName$(scrapy.Spider):

    name = '$spiderName$' # 必须, 对应的使用 scrapy crawl <name> 指令运行爬虫
    $nextStep$