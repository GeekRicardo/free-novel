#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as Soup
import time
from tqdm import tqdm

from . import Spider 


class XBQGSpider2(Spider):
    def __init__(self):
        super().__init__()
        self.process = 1
        self.catalen = 1 
        self.base_url = 
