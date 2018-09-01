# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Item(scrapy.Item):
    # define the fields for your item here like:
    spider_name=scrapy.Field()
    date=scrapy.Field()
    keyword=scrapy.Field()
    city=scrapy.Field()
    shop_id=scrapy.Field()
    url = scrapy.Field()
    company=scrapy.Field()
    user_name=scrapy.Field()
    mobile=scrapy.Field()
    addr=scrapy.Field()
    start_time=scrapy.Field()
    what=scrapy.Field()
    money=scrapy.Field()
    other=scrapy.Field()
    

class Item_ex(scrapy.Item):
    # define the fields for your item here like:
    spider_name=scrapy.Field()
    date=scrapy.Field()
    keyword=scrapy.Field()
    city=scrapy.Field()
    url = scrapy.Field()
    name=scrapy.Field()
    legal_person=scrapy.Field()
    log_money=scrapy.Field()
    log_date = scrapy.Field()
    contact = scrapy.Field()
    status=scrapy.Field()

    code = scrapy.Field()
    log_addr = scrapy.Field()
    company_type=scrapy.Field()
    bs_type=scrapy.Field()

    employee=scrapy.Field()
    canbao_people=scrapy.Field()






