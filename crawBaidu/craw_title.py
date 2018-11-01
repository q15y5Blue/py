# -*- coding: utf-8 -*-
# 爬主题
import time
import datetime
from crawBaidu.conection import BaseSession
from crawBaidu.craw_proxy import NetProtocol
from crawBaidu.db import DBConnect
from bs4 import Tag
from crawBaidu.entity import *
import requests
import re
from bs4 import BeautifulSoup
url_article = "https://tieba.baidu.com/f?kw=%CB%AB%C3%CE%D5%F2&pn=0&"

class crawArticle(object):
    def parserArticle(self, url):
        beSession = BaseSession()
        proxy = NetProtocol()
        req = beSession.reqGet(url=url, proxies=proxy)
        soup = BeautifulSoup(req.text, "html.parser")
        list = soup.find_all('li',class_='tl_shadow tl_shadow_new')
        # print(list)
        articleList = []
        for result in list:
            ar = article()
            ar.title = result.find('div',class_='ti_title').text.strip()
            ar.date = getTime(result.find('span', class_='ti_time').text.strip())
            ar.id = result.find('a', class_='j_common ti_item')['tid'].strip()
            ar.username = result.find('span', class_='ti_author').text.strip()
            articleList.append(ar)
        self.importArticle(articleList)

    def importArticle(self, list):
        conn = DBConnect()
        for ar in list:
            flag = conn.get_date("select id from article where id = '%s' " % ar.id)
            if flag is None:
                sql = "insert into article(id,title,username,date)  values('%s','%s','%s','%s') "%(ar.id, ar.title, ar.username, ar.date)
                print(sql)
                conn.update_info(sql)

    def parseReplyDetails(self, id):
        url = "https://tieba.baidu.com/p/%s" %(id)
        beSession = BaseSession()
        proxy = NetProtocol()
        req = beSession.reqGet(url=url, proxies=proxy)
        soup = BeautifulSoup(req.text, "html.parser")
        list = soup.find('ul', id='pblist').find_all('li', class_='list_item')
        for li in list:
            print(li)

def getTime(timeStr):
    tiRe = re.compile('\d\d:\d\d')
    if (tiRe.match(timeStr)):
        nowDate = datetime.datetime.now().date()
        dateStr = str(nowDate) + ' ' + timeStr
        return dateStr

if __name__=='__main__':
    # ar = crawArticle()
    # ar.parseReplyDetails('5923662453')
    # ar.parserArticle(url_article)
    values = u"sra3636"
    print(values)
    # print(values.decode('utf-8'))