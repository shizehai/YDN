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
    keyword=scrapy.Field()
    keyword=scrapy.Field()
    title=scrapy.Field()
    site_url=scrapy.Field()
    site_name=scrapy.Field()
    group=scrapy.Field()
    rel_time=scrapy.Field()
    content=scrapy.Field()
    




