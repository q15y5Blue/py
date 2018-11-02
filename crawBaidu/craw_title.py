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
import json
import re
from bs4 import BeautifulSoup

class crawArticle(object):
    def __init__(self):
        self.baseUrl = 'https://tieba.baidu.com/f?kw=%CB%AB%C3%CE%D5%F2&pn=0&'
        self.articleUrl = 'https://tieba.baidu.com/p/%s?pn=%s&'

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

    def parseReplyDetails(self, id,page):
        url = self.articleUrl %(id,page)
        beSession = BaseSession()
        proxy = NetProtocol()
        req = beSession.reqGet(url=url, proxies=proxy)
        soup = BeautifulSoup(req.text, "html.parser")
        pageNumer = soup.find('div', id='list_pager')
        list = soup.find('ul', id='pblist').find_all('li', class_='list_item')
        replyList = []
        for li in list:
            rp=reply()
            userinf = li['data-info']
            userinfo = json.loads(userinf)
            rp.author = userinfo['un']
            rp.id = userinfo['pid']
            rp.floor_num = userinfo['floor_num']
            rp.content = li.find('div', class_='content').prettify()
            rp.date = getTime(li.find('span', class_='list_item_time').text.strip())
            rp.child = []
            childList = li.find('ul', class_='flist') # 有flist属性才会有回复
            if childList is not None:
                if li.find('a', class_='fload_more_btn') is not None:
                    lp = self.parseDetailsOfReply(rp.id)
                    if(len(list)>0):
                        rp.child.extend(lp)
                else:
                    for child in childList:
                        # li of child
                        if type(child).__name__=='Tag':
                            chi = reply()
                            usinf = child['data-info']
                            usinfo = json.loads(usinf)
                            chi.author = usinfo['un']
                            chi.id = usinfo['pid']
                            chi.fn = rp.id
                            rp.child.append(chi)
            replyList.append(rp)
        return replyList

    # 输入reply.id,返回list
    def parseDetailsOfReply(self, id):
        url = "https://tieba.baidu.com/mo/q/post/floor/%s"%id
        beSession = BaseSession()
        proxy = NetProtocol()
        req = beSession.reqGet(url=url, proxies=proxy)
        soup = BeautifulSoup(req.text, "html.parser")
        ulList = soup.find('ul', class_='pb_lzl_content j_floor_panel').find_all('li')
        list = []
        for li in ulList:
            repl = reply()
            userinf = li['data-info']
            userinfo = json.loads(userinf)
            repl.id = userinfo['pid']
            repl.author = userinfo['un']
            repl.child = li.find('span',class_='lzl_content').text.strip()
            repl.date=getTime(li.find('p').text.strip())
            list.append(repl)
        return list

    def crawReplyExecute(self, articleId):
        replyList = []
        firstId = ''
        for page in range (0,30000):
            list = self.parseReplyDetails(articleId, page)
            if len(list)>0:
                if firstId == list[0].id:break
                firstId = list[0].id
            else:
                break

def getTime(timeStr):
    todays =str(datetime.datetime.now().date())
    toyearStr = str(datetime.datetime.now().year)
    if '今天' in timeStr:
        timeStr = timeStr.replace("今天", todays)
    todayRe = re.compile('\d\d:\d\d')
    monthRe = re.compile('\d\d-\d\d.*\d\d:\d\d')
    yearRe = re.compile('\d{4}-\d{2}-\d{2}.*\d\d:\d\d')
    if (todayRe.match(timeStr)):
        dateStr = todays + ' ' + timeStr
        return dateStr
    elif monthRe.match(timeStr):
        dataStr = toyearStr+"-"+str(timeStr)
        return dataStr
    elif yearRe.match(timeStr):
        return timeStr

if __name__=='__main__':
    # print(datetime.datetime.now().year)
    ar = crawArticle()
    ar.crawReplyExecute('5570271280')