# -*- coding: utf-8 -*-
# 爬主题
import time
import datetime
from crawBaidu.conection import BaseSession
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
    def parserArticle(self):
        beSession = BaseSession()
        req = beSession.reqGet(url=self.baseUrl, proxies=True)
        soup = BeautifulSoup(req.text, "html.parser")
        list = soup.find_all('li',class_='tl_shadow tl_shadow_new')
        articleList = []
        for result in list:
            ar = article()
            ar.title = result.find('div',class_='ti_title').text.strip()
            ar.date = getTime(result.find('span', class_='ti_time').text.strip())
            ar.id = result.find('a', class_='j_common ti_item')['tid'].strip()
            ar.username = result.find('span', class_='ti_author').text.strip()
            ar.replyList = self.crawReplyExecute(ar)
            self.importArticle(ar)
            # articleList.append(ar)
        # return articleList

    def parseReplyDetails(self, articleObj, page):
        beSession = BaseSession()
        url = self.articleUrl %(articleObj.id, str(page))
        req = beSession.reqGet(url=url,proxies=True)# , proxies=True
        soup = BeautifulSoup(req.text, "html.parser")
        list = soup.find('ul', id='pblist').find_all('li', class_='list_item')
        replyList = []
        childRsList = [] # 回复的回复，child of reply
        for li in list:
            rp=reply()
            userinf = li['data-info']
            userinfo = json.loads(userinf)
            rp.author = userinfo['un']
            rp.id = userinfo['pid']
            rp.floor_num = userinfo['floor_num']
            rp.content = li.find('div', class_='content').text.strip()
            rp.date = getTime(li.find('span', class_='list_item_time').text.strip())
            # 对于回复的回复，并不再添加一层，而是并列与父类在一层
            childList = li.find('ul', class_='flist') # 有flist属性才会有回复
            if childList is not None:
                if li.find('a', class_='fload_more_btn') is not None:
                    lp = self.parseDetailsOfReply(articleObj, repd=rp)
                    if(len(lp)>0):
                        childRsList.extend(lp)
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
                            # chi.articleId = rp.id
                            childRsList.append(chi)
            replyList.append(rp)
        replyList.extend(childRsList)
        return replyList

    # 获取评论的回复
    def parseDetailsOfReply(self, article, repd):
        url = "https://tieba.baidu.com/mo/q/post/floor/%s" % repd.id
        beSession = BaseSession()
        # proxy = NetProtocol()
        req = beSession.reqGet(url=url,proxies=True)# , proxies=proxy
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
                repl.content = li.find('span', class_='lzl_content').text.strip()
                repl.date=getTime(li.find('p').text.strip())
                repl.fn = repd.id
                # repl.articleId = article.id
                childList.append(repl)
                # print(repl) test Message
            list.extend(childList)
        return list

    def crawReplyExecute(self, article):
        beSession = BaseSession()
        articleInfoUrl = self.articleDetails % (article.id, str(0))
        infoJson = beSession.reqGet(articleInfoUrl, proxies=True).json()
        totalPage = int(infoJson['data']['page']['total_page'])
        rsList = []
        if totalPage >= 1:
            for nowPage in range(1, totalPage+1):
                list = self.parseReplyDetails(articleObj=article, page=nowPage)
                rsList.extend(list)
        return rsList

    def importArticle(self, ar):
        conn = DBConnect()
        flag = conn.get_date("select id from article where id = '%s' " % ar.id)
        if flag is None:
            print("insert a article")
            sql = "insert into article(id,title,username,date)  values('%s','%s','%s','%s') " % (
            ar.id, ar.title, ar.username, ar.date)
            conn.update_info(sql)
            # print(sql)
            self.importReply(ar)

    def importReply(self,art):
        con = DBConnect()
        for li in art.replyList:
            # print("insert a reply")
            flag = con.get_date("select id from reply where id = '%s' " %li.id)
            if flag is None:
                li.fn = 0 if li.fn == "" else li.fn
                li.floor_num = -1 if li.floor_num == "" else li.floor_num
                li.date = art.date if li.date == "" or li.date == None  else li.date
                sql = "insert into reply(id,content,author,date,floor_num,fn,articleId)values('%s','%s','%s','%s','%s','%s','%s')"%(
                    li.id,li.content,li.author,li.date,li.floor_num, li.fn, art.id)
                print(sql)
                con.update_info(sql)


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
    ar.parserArticle()
    # ar.crawReplyExecute('5570271280')
    # article = article()
    # article.id = '5937421881'
    # list = ar.crawReplyExecute(article=article)
    # print(len(list))
    # for res in list :
    #     print(res)