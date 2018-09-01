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
from CompanyInfo.items import Item,Item_ex


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
def cookie_str_to_dict(cookies_str):
    COOKIES={}
    tmp=cookies_str.split(';')
    for item in tmp:
        key_value=item.split('=')
        COOKIES[key_value[0]]=key_value[1]
    return COOKIES
cookie_str='TYCID=8207de4095f511e88a7d252ba3261424; undefined=8207de4095f511e88a7d252ba3261424; ssuid=6374018544; _ga=GA1.2.1441971809.1533174235; jsid=SEM-BAIDU-CG-SY-002211; _gid=GA1.2.1027893869.1535345936; RTYCID=cd82182144c247ad8bf6840a4f05d840; CT_TYCID=fc572b075f344f3ba23c82d3e4e27957; aliyungf_tc=AQAAAMSZ2gQt/QsASg9BcV12TfQLLYGY; csrfToken=xfM4tUrldL46YRL-XawlASz1; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1533174234,1534384253,1535345936,1535423041; bannerFlag=true; token=a60ca595a7e04921a1c1b7f6a5f7816c; _utm=aaa644903ee34b18a8ab8bab9d11573a; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTgxMzM2Mjg5NSIsImlhdCI6MTUzNTQyNTQ1MywiZXhwIjoxNTUwOTc3NDUzfQ.xH9SCMN2Ea7kr5Oiu4EOc8S6s3ZHyM50dXBTm_tV7n5GQOPYRq1juPGaCgw0vWspf2rJrpPvcI4mg-kpQ0HHow%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252215813362895%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTgxMzM2Mjg5NSIsImlhdCI6MTUzNTQyNTQ1MywiZXhwIjoxNTUwOTc3NDUzfQ.xH9SCMN2Ea7kr5Oiu4EOc8S6s3ZHyM50dXBTm_tV7n5GQOPYRq1juPGaCgw0vWspf2rJrpPvcI4mg-kpQ0HHow; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1535436487; cloud_token=f173a649505947b18feb8f2ed6b7df9f'

COOKIES=cookie_str_to_dict(cookie_str)

class alibaba(scrapy.Spider):

    name = 'alibaba' # 必须, 对应的使用 scrapy crawl <name> 指令运行爬虫
    # drive = webdriver.Chrome(executable_path=u'D:\\ProgramData\\chromedriver.exe', )
    # url='https://login.taobao.com/member/login.jhtml?style=mini&css_style=b2b&from=b2b&full_redirect=true&redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttp%25253A%25252F%25252Flogin.1688.com%25252Fmember%25252FtaobaoSellerLoginDispatch.htm&reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3Flead%3Dhttp%253A%252F%252Flogin.1688.com%252Fmember%252FtaobaoSellerLoginDispatch.htm%26leadUrl%3Dhttp%253A%252F%252Flogin.1688.com%252Fmember%252FtaobaoSellerLoginDispatch.htm%26tracelog%3Dlogin_s_reg'
    # drive.get(url)
    # drive.find_element_by_id("TPL_username_1").click()
    # time.sleep(0.3)
    # drive.find_element_by_id("TPL_username_1").send_keys("lmeastboy")
    # time.sleep(0.3)
    #

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
            print 'A'*30
            self.drive.find_element_by_xpath(".//*[@id='sw_mod_pagination_content']/div/a[11]").click()
        except:
            print 'B'*30
        self.drive.execute_script("window.scrollBy(0,500)", "")

        # time.sleep(2)
        # self.drive.execute_script("window.scrollBy(0,1000)", "")
        self.drive.get(url)
        time.sleep(10)
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
            self.drive.close()
            time.sleep(3)
            self.drive = webdriver.Chrome(executable_path=u'D:\\ProgramData\\chromedriver.exe', )
            self.drive.get('https://www.1688.com/')
            time.sleep(2)
            for cookie in self.cookies:
                self.drive.add_cookie(cookie)
            time.sleep(2)

            keyword_encode = urllib.quote(keyword.encode('GBK'))
            last_url = last_url_.format(keyword=keyword_encode, page=str(page))
            req = scrapy.Request('https://www.baidu.com/', callback=self.parse_list_item, dont_filter=True)
            req.meta['item'] = copy.deepcopy(item)
            req.meta['page'] = copy.deepcopy(page)
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
            req.meta['page'] = copy.deepcopy(page)
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


headers={
            'Accept':'application/json, text/plain, */*',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.tianyancha.com',
            'User_Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'X-Requested-With':'XMLHttpRequest',
        }

class tianyancha(scrapy.Spider):

    name = 'tianyancha' # 必须, 对应的使用 scrapy crawl <name> 指令运行爬虫

    def start_requests(self):
        with codecs.open('keywords.csv',encoding='utf-8') as fr:
            keywords = fr.readlines()
        page = 1
        for keyword in keywords:
            keyword=keyword.replace('\n','')
            url_='https://www.tianyancha.com/search/p{page}?key={keyword}'
            # keyword_encode=urllib.quote(keyword.encode('GBK'))
            url = url_.format(keyword=keyword, page=str(page))
            item = Item_ex()
            item['keyword'] = keyword
            item['date']=datetime.datetime.now().strftime('%Y-%m-%d')
            item['spider_name']=self.name
            req = scrapy.Request(url,callback=self.parse_list_item,headers=headers)
            req.meta['page'] = page
            req.meta['item'] = copy.deepcopy(item)
            req.meta['url_'] = copy.deepcopy(url_)

            yield req

    def parse_list_item(self, response):
        item = copy.deepcopy(response.meta['item'])
        page = response.meta['page']
        keyword=item['keyword']
        url_=response.meta['url_']

        text=response.text
        soup=BeautifulSoup(text)
        lines=soup.find_all(class_="search-result-single ")
        count=len(lines)
        # 翻页
        if count==20:
            page=page+1
            url = url_.format(keyword=keyword, page=str(page))
            req = scrapy.Request(url, headers=headers,callback=self.parse_list_item)
            req.meta['page'] = page
            req.meta['item'] = copy.deepcopy(item)
            req.meta['url_'] = copy.deepcopy(url_)
            yield req

        for line in lines:
            # 解析 item 数据
            content=line.find(class_='content')
            tmp=content.find("a")
            name=tmp.get_text()

            href=tmp.get('href')
            tmp=content.find(class_="num-opening")
            status=tmp.get_text()
            tmp=line.find(class_="site")
            city=tmp.get_text()
            tmp_list=line.find(class_="info").find_all(class_='title')

            legal_person=tmp_list[0].get_text()
            log_money=tmp_list[1].get_text()
            log_date=tmp_list[2].get_text()
            tmp=line.find(class_="contact")
            contact=tmp.get_text()

            item['name']=name
            item['url']=href
            item['status']=status
            item['city']=city
            item['legal_person']=legal_person
            item['log_money']=log_money
            item['log_date'] = log_date
            item['contact'] = contact
            req = scrapy.Request(href, cookies=COOKIES,headers=headers,callback=self.parse_item)
            req.meta['item'] = copy.deepcopy(item)
            yield req

    def parse_item(self, response):
        item = copy.deepcopy(response.meta['item'])
        text=response.text

        soup = BeautifulSoup(response.text,"lxml")
        name=soup.find('h1').get_text()
        log_addr=soup.find(colspan="4").get_text()
        company_type=text.split('公司类型</td><td>')[-1].split('<')[0]
        bs_type=soup.find(colspan="2").get_text()
        code=text.split('</td><td>公司类型')[0].split('>')[-1]

        item['name'] = name
        item['log_addr']=log_addr
        item['company_type'] = company_type
        item['bs_type'] = bs_type
        item['code'] = code


        yield item
