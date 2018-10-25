# -*- coding: utf-8 -*-
# 爬主题
import time
from crawBaidu import db as din
from crawBaidu import headers as hds
import requests
from bs4 import BeautifulSoup
url = "https://tieba.baidu.com/f?kw=%CB%AB%C3%CE%D5%F2&pn=0&"

class article(object):
    def __init__(self):
        self.id = ''
        self.title =''
        self.content = ''
        self.author = ''
        self.date = ''
        self.replyId = ''  # 5887786331这类的

    def crawArticle(self, url):
        return ''

class reply(object):
    def __init__(self):
        self.id = ''
        self.content=''
        self.author=''
        self.date = ''
        self.level= ''  # 楼层
        self.parents = ''  # 父级
