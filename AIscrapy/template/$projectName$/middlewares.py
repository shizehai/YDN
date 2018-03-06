# -*- coding: utf-8 -*-

'''
该文件可直接复制使用, 但需要在 settings.py 中进行相应设置:
USER_AGENTS, PROXIES, DOWNLOADER_MIDDLEWARES
'''

import random
from settings import USER_AGENTS
from settings import PROXIES
import logging

class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENTS)
        if ua:
            logging.debug("Current User-Agent: " + ua)
            request.headers.setdefault('User-Agent', ua)
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        logging.debug('Current proxy: %s' % proxy['ip'])
        request.meta['proxy'] = "http://%s" % proxy['ip']
        if proxy['password']!='':
            encoded_user_pass = base64.encodestring(proxy['password'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
