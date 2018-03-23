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
from CompanyInfo.settings import MONGODB_IP,MONGODB_DB,MONGODB_TABLE
from selenium import webdriver
# 导入 items 下面的自定义 Item 类
from CompanyInfo.items import Item

# try:
#   from map.items import mapItem
# except Exception as e:
#     print e
#lmeastboy
def cookie_str_to_dict(cookies_str):
    COOKIES={}
    tmp=cookies_str.split(';')
    for item in tmp:
        key_value=item.split('=')
        COOKIES[key_value[0]]=key_value[1]
    return COOKIES
cookie_str='UM_distinctid=1624d0052283ed-08fe61c952061f8-1269624a-100200-1624d00522a54f; cna=PK0rEkDTckYCATo+zK9Y6Ijy; isg=BBcXOF1eAdor0YVRLaWvPdsJpYuh9Os3D-T7kWlEQ-ZJmDbacShGDon6_riGa8M2; ali_ab=58.62.205.233.1521710288954.8; alicnweb=homeIdttS%3D71583866516567953900986988134051546885%7Ctouch_tb_at%3D1521784226080%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3Dlmeastboy; ad_prefer="2018/03/23 14:19:10"; h_keys="niuzaiku#%u4e1c%u839e#%u7537T%u6064#%u7537%u88c5"; alisw=swIs1200%3D1%7C; ali_beacon_id=58.62.205.233.152171061644.078830.1; last_mid=b2b-87075679; __last_loginid__=lmeastboy; _cn_slid_=z32rNqg27%2F; cn_tmp.sig=hvMgNhgiUUzXhaEflHcWqKDxU0GeBufkCOLSAkh4jDA; cn_m_s.sig=_wavPcna-gOpurUdYp3Gr9ZjXOQaLC1EcgZVgtB6Oxs; ali_apache_track.sig=cE13ut9KHyEt3zkFppskZzVrXvaZS2vbMOo270efb4c; __cn_logon_id__.sig=3DszBWnLBvy16IGzJrU4cEyzibSvzqhp8dvu1Qg3lRs; ali-ss=eyJtZW1iZXJJZCI6bnVsbCwidXNlcklkIjpudWxsLCJsb2dpbklkIjpudWxsLCJzaWQiOm51bGwsImVjb2RlIjpudWxsLCJsb2dpblN0YXR1c1JldE1zZyI6bnVsbCwibG9naW5NZXNzYWdlRXJyb3IiOm51bGwsImxvZ2luRXJyb3JVc2VyTmFtZSI6bnVsbCwiY2hlY2tjb2RlIjpudWxsLCJzZWNyZXQiOiJZNTFjd0d6aU5STURlSC05aER6M1UxMlciLCJfZXhwaXJlIjoxNTIxODcxNTE4NDIxLCJfbWF4QWdlIjo4NjQwMDAwMH0=; webp=0; _m_h5_tk=64255af548b509dc42c3c40411ca1230_1521787090192; _m_h5_tk_enc=bd84ac6aceba93a1931138d6b23b7a1e; ali_apache_id=11.130.127.209.1521711225908.276176.1; JSESSIONID=qi9ZhIe-voPZTnVRIqYeXcVET7-veFz4nQ-f0g; _tmp_ck_0=NY1Y64rIBuCuT5s1qqP%2Fp7QBlse9WbAZsPiE5T%2F2NKEMToPX25bZw6YEnwRSxSYLUpT%2Fm6nlC%2Fo%2F%2Fe7wHgh%2B0imyOFNU3GqcM4qjCqJmAzDaPACJoUznx2A%2F0mEohaohFe1P1REpELoTuf0I1j63lPD2u4YvLP7X8DqJbFj9K4huDCeuCbLCZc536Lo%2BV%2BR9jqDQnyO1C99mPOCqUwHX9BDSY9E6tFL1QpRrKoH%2BArIutOErgtNCy8rBRRzO77hAss0ir%2BKj61YE2CcMtn9i1iMgnVeu8ClAvbtEM7ZiJ4gKDHcGfqx4VXUt2QrDmCoNNIVqj5H99stBt8FyWkOV0PIWD3kap%2FPzItu9AHyNfMXtFhsbMQ3KYinE3wQZ5n3u4jpJ5zIb9dah2xp4EslOyemXJgBZXtrXT3xsLnhfY3YvuqkHlk6F7IhoS9cS9h5AzUD%2BFWfubeSjQgHHNDhqP03DdxXgr8OiyxvPQBxngy%2BSzoPN1yt4Ja1AaXZiaYYBvaOyDrWr5Y8%3D; __cn_logon__=false; _csrf_token=1521773723245; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=HIVsOEbQBTPi3wdaF8pnlF3pICU94Kf0o4yv9C3wKL4ogBSl%2FbuCDg%3D%3D; userID=XdggMZBWjIsFNXQye%2Fx3LRgKuADUlOGuKuz6VSpnjDI6sOlEpJKl9g%3D%3D; userIDNum=3zXgccP7ges6sOlEpJKl9g%3D%3D; ctoken=3tf1vEMAkkPYAAxv40PTzealot; _sync_time_=1521785105144; _sync_time_.sig=Qp3O-ERo3bZmzfC2DVRZ-UOsr9a0oPMIQd_qjsfLcso'
COOKIES=cookie_str_to_dict(cookie_str)

class alibaba(scrapy.Spider):

    name = 'alibaba' # 必须, 对应的使用 scrapy crawl <name> 指令运行爬虫
    drive = webdriver.Chrome(executable_path=u'D:\\ProgramData\\chromedriver.exe', )
    drive.get('https://login.1688.com/member/signin.htm')
    time.sleep(2)
    headers={
            'Accept':'application/json, text/plain, */*',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'s.1688.com',
            'User_Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'X-Requested-With':'XMLHttpRequest',
        }

    def start_requests(self):
        with codecs.open('keywords.csv',encoding='utf-8') as fr:
            keywords = fr.readlines()
        page = 1
        for keyword in keywords:
            keyword=keyword.replace('\n','')
            url_='https://s.1688.com/company/company_search.htm?keywords={keyword}&n=y&&city=%B6%AB%DD%B8&sortType=pop&pageSize=30&offset=3&beginPage={page}'
            keyword_encode=urllib.quote(keyword.encode('GBK'))
            url = url_.format(keyword=keyword_encode, page=str(page))
            item = Item()
            item['keyword'] = keyword
            item['date']=datetime.datetime.now().strftime('%Y-%m-%d')
            item['spider_name']=self.name
            req = scrapy.Request('https://www.baidu.com/',callback=self.parse_list_item)
            req.meta['page'] = page
            req.meta['item'] = copy.deepcopy(item)
            req.meta['url_'] = copy.deepcopy(url_)
            req.meta['url'] = copy.deepcopy(url)
            req.meta['all'] = 0
            yield req
        
    def parse_list_item(self, response):
        item = copy.deepcopy(response.meta['item'])
        page = response.meta['page']
        all = response.meta['all']
        keyword=item['keyword']
        last_url_=response.meta['url_']
        url=response.meta['url']

        # response文本预处理
        try:
            self.drive.find_element_by_xpath(".//*[@id='sw_mod_pagination_content']/div/a[11]").click()
        except:
            self.drive.get(url)
        time.sleep(11)
        text=self.drive.page_source
        soup=BeautifulSoup(text)
        lines=soup.find_all(class_="company-list-item")
        #防止异常

        if int(page)==1:
            tmp = soup.find(class_="sm-navigatebar-count")

            if tmp:
                all = tmp.get_text()
                if all.isdigit():
                    all = int(all)
                else:
                    all = 0
        if text.find(u'现您的网络环境')>1:
            keyword_encode = urllib.quote(keyword.encode('GBK'))
            last_url = last_url_.format(keyword=keyword_encode, page=str(page))
            req = scrapy.Request('https://www.baidu.com/', callback=self.parse_list_item, dont_filter=True)
            req.meta['item'] = copy.deepcopy(item)
            req.meta['page'] = page
            req.meta['url_'] = copy.deepcopy(last_url_)
            req.meta['url'] = copy.deepcopy(last_url)
            req.meta['all'] = copy.deepcopy(all)
            time.sleep(60)
            yield req

        # 翻页
        if all >30*int(page) :

            page=str(int(page)+1)
            keyword_encode = urllib.quote(keyword.encode('GBK'))
            last_url=last_url_.format(keyword=keyword_encode, page=str(page))
            req = scrapy.Request('https://www.baidu.com/',callback=self.parse_list_item,dont_filter=True)
            req.meta['item'] = copy.deepcopy(item)
            req.meta['page'] = page
            req.meta['url_'] = copy.deepcopy(last_url_)
            req.meta['url'] = copy.deepcopy(last_url)
            req.meta['all'] = copy.deepcopy(all)
            yield req

        for line in lines:

            # 解析 item 数据
            uri=line.find('a').get('href')
            shop_id=uri.split('.')[0].replace('https://','')

            info_url='https://{shop_id}.1688.com/page/creditdetail.htm'.format(shop_id=shop_id)
            item['shop_id']=shop_id
            item['url'] = info_url
            # yield item
            req = scrapy.Request(info_url, cookies=COOKIES,callback=self.parse_item)
            req.meta['item'] = copy.deepcopy(item)

            yield req
    

    def parse_item(self, response):
        item = copy.deepcopy(response.meta['item'])
        
        soup = BeautifulSoup(response.text)

        company=soup.find(class_="company-name").get_text()
        tmp=soup.find_all(class_="tip-info phone-num")
        mobile='*'
        m=re.findall(r'value=\"[0-9]{11}',response.text)
        if len(m)>0:
            mobile=m[0].replace('value="','')
        elif len(tmp)>1:
            mobile=tmp[-1].get_text().replace(u'手机号码：','')
        elif len(tmp)==1:
            mobile = tmp[0].get_text()
        tmp=soup.find(class_="contact-info")
        user_name='*'
        if tmp:
            user_name =tmp.get_text()

        start_time = '*'
        money = '*'
        what = '*'
        addr = '*'
        tmp=soup.find(class_="info-box info-right")
        if tmp:
            infos=tmp.find_all('tr')
            start_time = infos[0].get_text()
            money = infos[1].get_text()
            what = infos[2].get_text()
            addr = infos[3].get_text()

        item['company']=company
        item['mobile'] = mobile
        item['user_name'] = user_name
        item['start_time'] = start_time
        item['money'] = money
        item['what'] = what
        item['addr'] = addr

        yield item