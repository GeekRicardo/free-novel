#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File     :  xsbiqugeSpider.py
@Time     :  2020/07/06 18:52:22
@Author   :  Ricardo
@Version  :  1.0
@Desc     :  新笔趣阁xsbiquge爬虫相关
'''

# import lib here

import random
import time
import requests
from bs4 import BeautifulSoup as Soup
from tqdm import tqdm

from . import Spider
import pdb


class XBQGSpider(Spider):
    BaseURL = 'https://vbiquge.com/'


    def __init__(self):
        self.process = 1
        self.catalen = 1
        super().__init__()

    def search(self, keyword):
        url = self.BaseURL + 'search.php?keyword=' + keyword
        res = self.request(url)
        # pdb.set_trace()
        if res:
            soup = Soup(res.text, 'html.parser')
            result_item = soup.select('.result-list>.result-game-item')
            if not len(result_item) == 0:
                results = []
                for r in result_item:
                    title = r.find('h3').text
                    room = r.find('h3').find('a')['href'].split('/')[-2]
                    desc = r.select('.result-game-item-desc')[0].text
                    # pdb.set_trace()
                    author = r.select('.result-game-item-info-tag')[0].select('span')[1].text
                    updatetime = r.select('.result-game-item-info-tag')[2].select('span')[1].text
                    lastc = r.select('.result-game-item-info-tag')[3].select('a')[0].text
                    results.append({
                        'title':title.replace('\r\n','').strip(),
                        'desc': desc.replace('\r\n','').strip(),
                        'author': author.replace('\r\n','').strip(),
                        'updatetime': updatetime.replace('\r\n','').strip(),
                        'lastc': lastc.replace('\r\n','').strip(),
                        'url': room})
                return results
            else:
                print('没有搜到结果')
                return None
        else:
            return None

    def getcatalogs(self, room):
        """获取目录
        """
        print('\n&&&&&请求目录&&&&&&\n')
        url = self.BaseURL + str(room) + '/'
        res = self.request(url)
        if(res):
            soup = Soup(res.text, 'html.parser')
            alltitle = soup.select('dd')
            catalogs = []
            for title in alltitle:
                catalogs.append((title.text, title.find('a')['href'].split('.')[0].split('/')[-1]))
            maininfo = {
                'img': soup.select('#fmimg')[0].find('img')['src'] or '',
                'title': soup.select('#info>h1')[0].text.replace('\r\n','').strip() or None,
                'author':soup.select('#info>p')[0].text.replace('\r\n','').strip() or None
            }
            return maininfo, catalogs
        else:
            return None, None

    def getContent(self, room, chapterid):
        url = self.BaseURL + str(room) + '/' + str(chapterid) + '.html'
        res = self.request(url)
        if res:
            soup = Soup(res.text, 'html.parser')
            title = soup.select('.bookname>h1')[0].text
            content = soup.select('#content')[0].text.split('\xa0\xa0\xa0\xa0')
            return (title, content)
        return None, None

    def getProcess(self):
        p = self.process/self.catalen
        return p

    def download(self, room, db, TXT, Chapter):
        self.process = -1
        self.catalen = 1
        maininfo, catalogs = self.getcatalogs(room)
        newTxt = TXT()
        newTxt.title = maininfo['title']
        newTxt.author = maininfo['author']
        newTxt.url = self.BaseURL + str(room) + '/'
        db.session.add(newTxt)
        db.session.flush()
        db.session.commit()
        if newTxt.id:
            self.catalen = len(catalogs)
            cats = tqdm(catalogs)
            for c in cats:
                title, content = self.getContent(room, c[1])
                if cats.last_print_n // 10 == 0:
                    self.logger.info("{} -> {}".format(self.getProcess(), title))
                if not content:
                    time.sleep(3)
                    self.getContent(room, c[1])
                    if not content:
                        time.sleep(10)
                        self.getContent(room, c[1])
                chapter = Chapter.newc(title, self.process, '\n'.join(content), newTxt.id)
                db.session.add(chapter)
                db.session.commit()
                self.process += 1


