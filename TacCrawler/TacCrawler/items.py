# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Item(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    spider_name=scrapy.Field()
    host=scrapy.Field()
    head_num=scrapy.Field()
    TAC = scrapy.Field()
    manufacturer=scrapy.Field()
    brand_model=scrapy.Field()




