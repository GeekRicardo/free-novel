#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File     :  spider.py
@Time     :  2020/07/06 18:53:28
@Author   :  Ricardo
@Version  :  1.0
@Desc     :  小说爬虫基类
'''

# import lib here
import random
import requests
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Spider():
    def __init__(self):
        super().__init__()
        url1 = 'http://www.xbiquge.la/'
        self.logger = logging.getLogger(__name__)

    def getheader(self):
        with open(os.path.abspath('txt/spiders/user_agents.txt'), 'r') as f:
            headers = []
            for l in f.readlines():
                headers.append(l.strip())
            return random.choice(headers)

    def request(self, url, proxy=False):
        try:
            res = None
            requests.packages.urllib3.disable_warnings()
            if proxy:
                proxies = {'http':self.getProxy(), 'https':self.getProxy()}
                res = requests.get(url, verify=False, headers={'User-Agent': self.getheader()}, proxies=proxies)
            else:
                res = requests.get(url, verify=False, headers={'User-Agent': self.getheader()})
            if res.status_code == 200:
                res.encoding = 'gbk2312'
                return res
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def getProxy(self):
        return "http://localhost:10809"
