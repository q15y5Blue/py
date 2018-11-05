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
    def __init__(self):#初始化的url都是有参数的
        self.baseUrl = 'https://tieba.baidu.com/f?kw=%CB%AB%C3%CE%D5%F2&pn=0&'
        self.articleDetails = "https://tieba.baidu.com/mo/q/m?kz=%s&is_ajax=1&post_type=normal&_t=1541397696480&pn=%s&is_ajax=1"
        self.articleUrl = 'https://tieba.baidu.com/p/%s?pn=%s&'
        self.detailsUrl = "https://tieba.baidu.com/mo/q/flr?fpn=%s&total_page=%s&kz=%s&pid=%s&is_ajax=1&has_url_param=0&template=lzl"

    # 主页面爬取多少个article
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

    def parseReplyDetails(self, articleObj, page):
        beSession = BaseSession()
        url = self.articleUrl %(articleObj.id, str(page*30) )
        req = beSession.reqGet(url=url, proxies=True)
        soup = BeautifulSoup(req.text, "html.parser")
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
                    lp = self.parseDetailsOfReply(articleObj, repd=rp)
                    if(len(lp)>0):
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

    # 获取评论的回复
    def parseDetailsOfReply(self, article, repd):
        url = "https://tieba.baidu.com/mo/q/post/floor/%s" % repd.id
        beSession = BaseSession()
        proxy = NetProtocol()
        req = beSession.reqGet(url=url, proxies=proxy)
        soup = BeautifulSoup(req.text, "html.parser")
        totalPage = int(soup.find('div', class_='pb_lzl_loading_more_bar')['total-page'])
        list = []
        for nowPage in range(1, totalPage+1):
            detailUrl = self.detailsUrl% (nowPage, totalPage, article.id, repd.id)
            reqDetais = beSession.reqGet(url=detailUrl, proxies=True)
            reJson = reqDetais.json()['data']['floor_html']
            liList = BeautifulSoup(reJson, "html.parser")
            childList= []
            for li in liList:
                repl = reply()
                userinf = li['data-info']
                userinfo = json.loads(userinf)
                repl.id = userinfo['pid']
                repl.author = userinfo['un']
                repl.content = li.find('span', class_='lzl_content').prettify().strip()
                repl.date=getTime(li.find('p').text.strip())
                childList.append(repl)
                # print(repl) test Message
            list.extend(childList)
        return list

    def crawReplyExecute(self, article):
        beSession = BaseSession()
        articleInfoUrl = self.articleDetails % (article.id, str(0))
        infoJson = beSession.reqGet(articleInfoUrl, proxies=True).json()
        print(infoJson)
        totalPage = int(infoJson['data']['page']['total_page'])
        rsList = []
        if totalPage >= 1:
            for nowPage in range(1, totalPage+1):
                list = self.parseReplyDetails(articleObj=article,page=nowPage)
                rsList.extend(list)
        return rsList


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
    ar = crawArticle()
    # ar.crawReplyExecute('5570271280')
    article = article()
    article.id = '5937421881'
    list = ar.crawReplyExecute(article=article)
    print(len(list))
    # for res in list :
    #     print(res)