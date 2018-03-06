# coding: utf-8
import pandas as pf
import os, sys, time
import shutil


class biliSpiderScrips(object):
    # 创建项目
    def createProject(self):
        shutil.copytree('template', 'out')
        os.chdir('out')  # 改变工作目录到template
        result = os.rename(u'$projectName$', self.projectName)  # 创建工程目录

        # 修改scrapy.cfg 文件
        with open('scrapy.cfg', 'a+') as fr:
            tmp = fr.read()
        tmp = tmp.replace('$projectName$', self.projectName)
        with open('scrapy.cfg', 'w') as fw:
            fw.write(tmp)
        time.sleep(0.5)

    # 配置settings
    def settings(self, mongodb_ip='192.168.11.17', mongodb_db='CrawlerData_other', mongodb_table='test'):
        # 修改settings 文件
        os.chdir(self.projectName)  # 改变工作目录到template
        with open('settings.py', 'a+') as fr:
            tmp = fr.read()
        tmp = tmp.replace('$projectName$', self.projectName)
        tmp = tmp.replace('$mongodb_ip$', mongodb_ip)
        tmp = tmp.replace('$mongodb_db$', mongodb_db)
        tmp = tmp.replace('$mongodb_table$', mongodb_table)
        with open('settings.py', 'w') as fw:
            fw.write(tmp)

    # 创建items
    def createItems(self, items):

        items_txt = ''
        for item in items:
            items_txt = items_txt + item + '=scrapy.Field()\n+    '
        with open('items.py', 'a+') as fr:
            tmp = fr.read()
        tmp = tmp.replace('$items$', items_txt.replace('+', ''))
        with open('items.py', 'w') as fw:
            fw.write(tmp)

    # 创建spider
    def createSpider(self):
        os.chdir('spiders')  # 改变工作目录到spiders
        # 修改scrapy.cfg 文件
        with open('Spider.py', 'a+') as fr:
            tmp = fr.read()
        tmp = tmp.replace('$projectName$', self.projectName)
        tmp = tmp.replace('$spiderName$', self.spiderName)
        with open('Spider.py', 'w') as fw:
            fw.write(tmp)

    def StartReqByKw(self, url_='www.example.com/{keyword}/{page}'):
        with open('Spider.py', 'a+') as fr:
            spiders_tmp = fr.read()
        req_tmp = '''
    def start_requests(self):
        with codecs.open('keywords.csv',encoding='utf-8') as fr:
            keywords = fr.readlines()
        page = 1
        for keyword in keywords:
            keyword=keyword.replace('\\n','')
            url_='$url_$'
            url = url_.format(keyword=keyword, page=str(page))
            item = Item()
            item['keyword'] = keyword
            req = scrapy.Request(url, callback=self.parse_list_item)
            req.meta['page'] = page
            req.meta['item'] = copy.deepcopy(item)
            req.meta['url_'] = copy.deepcopy(url_)
            yield req
        '''
        spiders_tmp = spiders_tmp.replace('$nextStep$', req_tmp)
        spiders_tmp = spiders_tmp.replace('$url_$', url_)
        with open('Spider.py', 'w') as fw:
            fw.write(spiders_tmp)

    def ParseHtml(self, res_meta_keys, line_keys, req_meta_keys, name='', next_step_type='item', callback='',
                  method='get', TP_page_limit=10, TP_count_limit=10, TP_method='get'):
        with open('nextStep.py', 'a+') as f:
            SC = f.read()
        SC = SC.replace('$name$', name)
        SC = SC.replace('$res_meta_keys$', self._create_res_meta(res_meta_keys))
        if TP_page_limit <> 0 and TP_count_limit <> 0:
            SC = SC.replace('$turn_page$', self._next_page(self.req_meta, method=TP_method, callback='self.' + name))
        SC = SC.replace('$line_keys$', self._create_lines_and_items(line_keys, self.items))
        SC = SC.replace('$to_next_step$',
                        self._to_next_step(next_step_type, req_meta=req_meta_keys, method=method, callback=callback))
        with open('Spider.py', 'a+') as f:
            f.write(SC)

    def ParseJson(self, res_meta_keys, line_keys, req_meta_keys, name='', next_step_type='item', callback='',
                  method='get', TP_page_limit=10, TP_count_limit=10, TP_method='get'):
        with open('nextStep.py', 'a+') as f:
            SC = f.read()
        SC = SC.replace('$name$', name)
        SC = SC.replace('$res_meta_keys$', self._create_res_meta(res_meta_keys))
        if TP_page_limit <> 0 and TP_count_limit <> 0:
            SC = SC.replace('$turn_page$', self._next_page(self.req_meta, method=TP_method, callback='self.' + name))
        SC = SC.replace('$line_keys$', self._create_lines_and_items_from_json(line_keys, self.items))
        SC = SC.replace('$to_next_step$',
                        self._to_next_step(next_step_type, req_meta=req_meta_keys, method=method, callback=callback))
        with open('Spider.py', 'a+') as f:
            f.write(SC)

    def _create_res_meta(self, res_meta, blank_n=8):
        script = ''
        for key in res_meta:
            script = script + key + "=response.meta['%s']\n" % key + " " * blank_n
        return script

    def _create_lines_and_items(self, lines, items, blank_n=12):
        script = ''
        for key in lines:
            script = script + key + "=line.find(class_='').find(class_='').get_text()\n" + " " * blank_n
        script = script + '\n' + " " * blank_n
        for key in items:
            if key in lines:
                script = script + "item['%s']=" % key + key + '\n' + " " * blank_n
        return script

    def _create_lines_and_items_from_json(self, lines, items, blank_n=12):
        script = ''
        for key in lines:
            script = script + key + "=line['%s']\n" % key + " " * blank_n
        script = script + '\n' + " " * blank_n
        for key in items:
            if key in lines:
                script = script + "item['%s']=" % key + key + '\n' + " " * blank_n
        return script

    def _create_req_meta_(self, req_meta, blank_n=12):
        script = ''
        for key in req_meta:
            script = script + "req.meta['{}']={}\n".format(key, key) + " " * blank_n
        return script

    def _next_page(self, req_meta, page_limit=10, count_limit=10, method='get', callback='self.parse'):

        script = '''
        if int(page) < $page$ or int(count) < $count$:
            page=str(int(page+1))
            last_url=last_url_.format(keyword=keyword, page=str(page))
            req = $method$
            req.meta['item'] = copy.deepcopy(item)
            req.meta['page'] = page
            req.meta['url_'] = copy.deepcopy(last_url_)
            $req_meta$
            yield req
    '''
        script = script.replace('$page$', str(page_limit)).replace('$count$', str(count_limit))
        if method.lower() <> 'post':
            method_sc = 'scrapy.Request(last_url, callback=$callback$)'.replace('$callback$', callback)
        else:
            method_sc = 'scrapy.FormRequest(last_url,formdata=formdata, callback=$callback$)'.replace('$callback$',
                                                                                                      callback)
        script = script.replace('$method$', method_sc)
        req_meta_sc = self._create_req_meta_(req_meta)
        script = script.replace('$req_meta$', req_meta_sc)
        return script

    def _to_next_step(self, next_step_type, req_meta=['items'], method='get', callback='self.parse'):
        # next_step_type:item or req
        if next_step_type == 'req':
            script = '''
            formdata={}
            url=url_
            req = $method$
            req.meta['item'] = copy.deepcopy(item)
            req.meta['page'] = page
            req.meta['url_'] = copy.deepcopy(url_)
            $req_meta$
            yield req
    '''
            if method.lower() <> 'post':
                method_sc = 'scrapy.Request(url, callback=$callback$)'.replace('$callback$', callback)
            else:
                method_sc = 'scrapy.FormRequest(url,formdata=formdata, callback=$callback$)'.replace('$callback$',
                                                                                                     callback)
            script = script.replace('$method$', method_sc)
            req_meta_sc = self._create_req_meta_(req_meta, 12)
            script = script.replace('$req_meta$', req_meta_sc)
        else:
            script = '''
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
                        item[key] = value.replace('\\t', '').replace('\\r', '').replace('\\n', '').strip()
            items = map(pre_process_item, items)
            # 修改数据库名、数据表名
            client = MongoClient(MONGODB_IP, 27017)
            # 修改数据库名、数据表名
            db = client[MONGODB_DB]
            db_key = db[MONGODB_TABLE]
            info = db_key.insert_many(items)

              '''
        return script

    def __call__(self, mapCrawler, spiderName, items, db_settings):
        self.projectName = mapCrawler
        self.spiderName = spiderName
        self.items = items
        self.req_meta = ['keyword']

        self.createProject()
        self.settings(db_set[0], db_set[1], db_set[2])
        self.createItems(self.items)
