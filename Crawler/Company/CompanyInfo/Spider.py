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
cookie_str='UM_distinctid=1624d0052283ed-08fe61c952061f8-1269624a-100200-1624d00522a54f; cna=PK0rEkDTckYCATo+zK9Y6Ijy; isg=BEhIJ1-Bht1zwupcxjjIGIAMGraaWa79RIEU3AL5lEO23ehHqgF8i97fUTWtdmTT; ali_ab=58.62.205.233.1521710288954.8; alicnweb=homeIdttS%3D71583866516567953900986988134051546885%7Ctouch_tb_at%3D1521894884792%7ChomeIdttSAction%3Dtrue%7Clastlogonid%3Dlmeastboy; ad_prefer="2018/03/24 21:07:16"; h_keys="niuzaiku#%u4e1c%u839e#%u7537T%u6064#%u7537%u88c5"; alisw=swIs1200%3D1%7C; ali_beacon_id=58.62.205.233.152171061644.078830.1; last_mid=b2b-87075679; __last_loginid__=lmeastboy; _cn_slid_=z32rNqg27%2F; webp=0; _m_h5_tk=64255af548b509dc42c3c40411ca1230_1521787090192; _m_h5_tk_enc=bd84ac6aceba93a1931138d6b23b7a1e; ali_apache_id=11.130.127.209.1521711225908.276176.1; ali_apache_track=c_mid=b2b-87075679|c_lid=lmeastboy|c_ms=1; JSESSIONID=9L78n5aw1-w1LZ7Qow68IHKG7EC6-yqoPDnQ-sgaF; _tmp_ck_0="LUGYM4%2BaK%2FXT7ITsPt3T5gOfVHi6toqL1juVgZ0a8M%2BXPNCJLteud9XIiEr%2Ffakzi3A0ytcehqCQRgmOolcZ4ZVTKzMix%2B8RCjyHKggJ66ucWuy7NpeP2LD5%2FAQ0PZfH3BJk7ecw%2F44E6G23PmnSSf1sN1hysNvHr7YbvOblJujNmowd0rYskGsGNopKGEcd02rGATJp8pCdskFjpOMWx%2FvPmnOu0%2BwqdxsNdzjuiCxznlRhZQNbclgLafseVe4hgsNuqN7O8pzU05xB8X7ixO%2BzMtTwwPQ%2BJpIP4OqCgcubCw6iBWcdxa8j8hn5uW%2F5zI1uLkVrIbOr48h0sOvQ0%2BzBHMaxznPBWrwVonXTiNbtW3Dh%2BGgeDLvvFnpn8EgTZjtHUfh4jUlhKBk6%2FhdmOrMg9V5brtQw2xkG5g%2FZMMmCSuixaO0L21DnIqxyasyYSy1%2FAOKOzmW2JpfBtNEQOIKiJg1XZksBMj8OVhLQ3Ae%2B9WeeTmsidFKepiqgRRkUTMP%2FZ2uDzEfF9rwD9zvSPQ%3D%3D"; __cn_logon__=true; cookie1=UIHxTlBMfcBw0VfDrE7DOvjPmOB5WHfFgBTCPR5aB1U%3D; cookie2=1fe69c093456f7d80eb36fcb8ca4c39d; cookie17=W8793cyGTxo%3D; hng=CN%7Czh-CN%7CCNY%7C156; t=9542805b36ce48f5ae1ee581b2570d4d; _tb_token_=ebc5e7bc5f1bb; sg=y9e; csg=b01f561d; __cn_logon_id__=lmeastboy; ali_apache_tracktmp=c_w_signed=Y; LoginUmid=HIVsOEbQBTPi3wdaF8pnlF3pICU94Kf0o4yv9C3wKL4ogBSl%2FbuCDg%3D%3D; unb=87075679; tbsnid=uAe%2FwAjH1Terxaqq5TD2MIi0SHbigj5mGUod011Zxzg6sOlEpJKl9g%3D%3D; cn_tmp="Z28mC+GqtZ00aIZUAwEEfYrv+0L9J3RXqCepgUxHoGOmc2CBy7+SyCk2RFIp37N9VVkW41Kk6keajLxdNyNBZg9FPfsDdrSIFZr9AhI9TQGCTSa70zL/AMtJTRZvPjqphwzJ886FP75eqnW7y5c2P39M8lwLSmoJIM5n+2bXpeAN+chR0814nJ+WFng44C28U5ogD6REWVV/NTXP6zRtDPs54ixDl1afKSGl9L/OpYw="; _csrf_token=1521896835983; login=kFeyVBJLQQI%3D; userID=XdggMZBWjIsFNXQye%2Fx3LRgKuADUlOGuKuz6VSpnjDI6sOlEpJKl9g%3D%3D; _nk_=ZdLFfrIqNYiQNYH3Kd64Ng%3D%3D; userIDNum=3zXgccP7ges6sOlEpJKl9g%3D%3D; _is_show_loginId_change_block_=b2b-87075679_false; _show_force_unbind_div_=b2b-87075679_false; _show_sys_unbind_div_=b2b-87075679_false; _show_user_unbind_div_=b2b-87075679_false; __rn_alert__=false'
COOKIES=cookie_str_to_dict(cookie_str)

class alibaba(scrapy.Spider):

    name = 'alibaba' # 必须, 对应的使用 scrapy crawl <name> 指令运行爬虫
    # drive = webdriver.Chrome(executable_path=u'D:\\ProgramData\\chromedriver.exe', )
    # drive.get('https://login.1688.com/member/signin.htm')
    # time.sleep(2)
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


class alibaba2(scrapy.Spider):
    name = 'alibaba2'  # 必须, 对应的使用 scrapy crawl <name> 指令运行爬虫

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 's.1688.com',
        'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'X-Requested-With': 'XMLHttpRequest',
    }

    def start_requests(self):
        with codecs.open('keywords.csv', encoding='utf-8') as fr:
            keywords = fr.readlines()
        page = 1
        for keyword in keywords:
            keyword = keyword.replace('\n', '')
            url_ = 'https://s.1688.com/company/company_search.htm?keywords={keyword}&n=y&&city=%B6%AB%DD%B8&sortType=pop&pageSize=30&offset=3&beginPage={page}'
            keyword_encode = urllib.quote(keyword.encode('GBK'))
            url = url_.format(keyword=keyword_encode, page=str(page))
            item = Item()
            item['keyword'] = keyword
            item['date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            item['spider_name'] = self.name
            req = scrapy.FormRequest(url, formdata={},cookies=COOKIES,callback=self.parse_list_item)
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
        keyword = item['keyword']
        last_url_ = response.meta['url_']
        url = response.meta['url']

        # response文本预处理

        text = response.text
        soup = BeautifulSoup(text,"lxml")
        lines = soup.find_all(class_="company-list-item")
        # 防止异常

        if int(page) == 1:
            tmp = soup.find(class_="sm-navigatebar-count")

            if tmp:
                all = tmp.get_text()
                if all.isdigit():
                    all = int(all)
                else:
                    all = 0
        if text.find(u'现您的网络环境') > 1:
            keyword_encode = urllib.quote(keyword.encode('GBK'))
            last_url = last_url_.format(keyword=keyword_encode, page=str(page))
            req = scrapy.FormRequest(url,  formdata={},callback=self.parse_list_item, cookies=COOKIES,dont_filter=True)
            req.meta['item'] = copy.deepcopy(item)
            req.meta['page'] = copy.deepcopy(page)
            req.meta['url_'] = copy.deepcopy(last_url_)
            req.meta['url'] = copy.deepcopy(last_url)
            req.meta['all'] = copy.deepcopy(all)
            print '*'*30
            yield req

        # 翻页
        if all > 30 * int(page):
            page = str(int(page) + 1)
            keyword_encode = urllib.quote(keyword.encode('GBK'))
            last_url = last_url_.format(keyword=keyword_encode, page=str(page))
            req = scrapy.FormRequest(url,  formdata={},callback=self.parse_list_item, cookies=COOKIES,dont_filter=True)
            req.meta['item'] = copy.deepcopy(item)
            req.meta['page'] = copy.deepcopy(page)
            req.meta['url_'] = copy.deepcopy(last_url_)
            req.meta['url'] = copy.deepcopy(last_url)
            req.meta['all'] = copy.deepcopy(all)
            yield req

        for line in lines:
            # 解析 item 数据
            uri = line.find('a').get('href')
            shop_id = uri.split('.')[0].replace('https://', '')

            info_url = 'https://{shop_id}.1688.com/page/creditdetail.htm'.format(shop_id=shop_id)
            item['shop_id'] = shop_id
            item['url'] = info_url
            # yield item
            req = scrapy.Request(info_url, cookies=COOKIES, callback=self.parse_item)
            req.meta['item'] = copy.deepcopy(item)

            yield req

    def parse_item(self, response):
        item = copy.deepcopy(response.meta['item'])

        soup = BeautifulSoup(response.text)

        company = soup.find(class_="company-name").get_text()
        tmp = soup.find_all(class_="tip-info phone-num")
        mobile = '*'
        m = re.findall(r'value=\"[0-9]{11}', response.text)
        if len(m) > 0:
            mobile = m[0].replace('value="', '')
        elif len(tmp) > 1:
            mobile = tmp[-1].get_text().replace(u'手机号码：', '')
        elif len(tmp) == 1:
            mobile = tmp[0].get_text()
        tmp = soup.find(class_="contact-info")
        user_name = '*'
        if tmp:
            user_name = tmp.get_text()

        start_time = '*'
        money = '*'
        what = '*'
        addr = '*'
        tmp = soup.find(class_="info-box info-right")
        if tmp:
            infos = tmp.find_all('tr')
            start_time = infos[0].get_text()
            money = infos[1].get_text()
            what = infos[2].get_text()
            addr = infos[3].get_text()

        item['company'] = company
        item['mobile'] = mobile
        item['user_name'] = user_name
        item['start_time'] = start_time
        item['money'] = money
        item['what'] = what
        item['addr'] = addr

        yield item