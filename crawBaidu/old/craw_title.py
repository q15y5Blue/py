# -*- coding: utf-8 -*-
# 爬主题
import time
import datetime
from crawBaidu.old.conection import BaseSession
from crawBaidu.old.db import DBConnect
from crawBaidu.old.entity import *
import json
import re
from bs4 import BeautifulSoup
from mysql.connector.errors import IntegrityError

class crawArticle(object):
    def __init__(self):#初始化的url都是有参数的
        self.baseUrl = "https://tieba.baidu.com/mo/q/m?kw=剑网3&pn=%d&lm=0&cid=0&has_url_param=0&is_ajax=1"
        self.articleDetails = "https://tieba.baidu.com/mo/q/m?kz=%s&is_ajax=1&post_type=normal&_t=%d&pn=%s&is_ajax=1"
        self.detailsUrl = "https://tieba.baidu.com/mo/q/flr?fpn=%s&total_page=%s&kz=%s&pid=%s&is_ajax=1&has_url_param=0&template=lzl"

    def parserArticle(self):
        baseSession = BaseSession()
        for pageNo in range(1):
            baseInfoUrl = self.baseUrl % (pageNo * 50)
            infoJson = baseSession.reqGet(baseInfoUrl, proxies=True).json()
            soup = BeautifulSoup(infoJson['data']['content'],'html.parser')
            list = soup.find_all('li', class_='tl_shadow tl_shadow_new')
            for result in list:
                ar = article()
                ar.title = result.find('div', class_='ti_title').text.strip()
                ar.date = getTime(result.find('span', class_='ti_time').text.strip())
                ar.id = result.find('a', class_='j_common ti_item')['tid'].strip()
                ar.username = result.find('span', class_='ti_author').text.strip()
                ar.user.img_path = result.find('img')['src']
                ar.user.username = result.find('span',class_='ti_author').text.strip()
                conn = DBConnect()
                flag = conn.get_date("select id from article where id = '%s' " % ar.id)
                if flag is None:
                    ar.replyList = self.crawReplyExecute(ar)
                    self.importArticle(ar, conn)
                else:
                    conn.closeCnt()
                    print("该Article已经存在，不再进行爬取。")


    def parseReplyDetails(self, articleObj,doc):
        soup = BeautifulSoup(doc, "html.parser")
        list = soup.find_all('li', class_='list_item')
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
            if rp.floor_num == 1 and articleObj.content == '':
                articleObj.content = rp.content
            rp.date = getTime(li.find('span', class_='list_item_time').text.strip())
            rp.user.username = li.find('span', class_="user_name").text.strip()
            rp.user.img_path = str(li.find('img', class_="user_img")['src']).replace("amp;", "")
            childList = li.find('ul', class_='flist') # 有flist属性才会有回复
            if childList is not None:
                if li.find('a', class_='fload_more_btn') is not None:
                    continue
                    # 拥有楼中楼
                    # lp = self.parseDetailsOfReply(articleObj, repd=rp)
                    # if(len(lp)>0):
                    #     childRsList.extend(lp)
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
                            chi.user.username = chi.author
                            # chi.articleId = rp.id
                            childRsList.append(chi)
            replyList.append(rp)
        replyList.extend(childRsList)
        return replyList

    # 楼中楼取消爬取,信息量小,速度慢
    # 获取评论的回复
    def parseDetailsOfReply(self, article, repd):
        url ="https://tieba.baidu.com/mo/q/flr?kz=%s&pid=%s&is_ajax=1&has_url_param=0&template=lzl" %(article.id, repd.id)
        beSession = BaseSession()
        req = beSession.reqGet(url=url,proxies=True).json() # , proxies=proxy
        list = []
        try:
            totalPage = req['data']['page']['total_page']
            # current_page = req['data']['page']['current_page']
        except Exception as exp:
            print(exp)
        if totalPage == 1 or totalPage=='1':
            childList = []
            liList = BeautifulSoup(req['data']['floor_html'], 'html.parser')
            for li in liList:
                repl = reply()
                userinf = li['data-info']
                userinfo = json.loads(userinf)
                repl.id = userinfo['pid']
                repl.author = userinfo['un']
                repl.content = li.find('span', class_='lzl_content').text.strip()
                repl.date = getTime(li.find('p').text.strip())
                repl.fn = repd.id
                repl.user.username = repl.author
                repl.user.img_path = str(li.find('img')['src'])
                childList.append(repl)
            list.extend(childList)
        else:
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
                    repl.user.username = repl.author
                    repl.user.img_path = str(li.find('img')['src'])
                    childList.append(repl)
                list.extend(childList)
        return list

    def crawReplyExecute(self, article):
        beSession = BaseSession()
        articleInfoUrl = self.articleDetails % (article.id, int(time.time()), str(0))# articleId time pn
        infoJson = beSession.reqGet(articleInfoUrl, proxies=True).json()
        totalPage = int(infoJson['data']['page']['total_page'])
        offSet = int(infoJson['data']['page']['page_size'])
        rsList = []
        for nowPage in range(1, totalPage+1):
            # print("nowPage",nowPage,"  totalPage",totalPage,"  offSet:",offSet)
            if nowPage ==1:
                doct = infoJson['data']['html']
                list = self.parseReplyDetails(articleObj=article, doc=doct)
                rsList.extend(list)
            else:
                articleMoreInfoUrl = self.articleDetails % (article.id, int(time.time()), str(offSet*nowPage))  # articleId time pn
                infoJson = beSession.reqGet(articleMoreInfoUrl, proxies=True).json()
                doct = infoJson['data']['html']
                list = self.parseReplyDetails(articleObj=article, doc=doct)
                rsList.extend(list)
        return rsList


    def importArticle(self, ar, Con):
        print("insert a article")
        userFlag = ar.user.checkUserByUserName(ar.username)
        # userFlag = Con.get_date("select id,username from users where username = '%s' "%ar.username)
        if userFlag is None:
            Con.update_info("insert into users(img_path,username) values ('%s','%s') "%(ar.user.img_path, ar.user.username))
            userFlag = ar.user.checkUserByUserName(ar.username)
        sql = "insert into article(id,title,user_id,date,content)  values('%s','%s','%s','%s','%s') " % (
            ar.id, ar.title, userFlag, ar.date,ar.content)
        Con.update_info(sql)
        self.importReply(ar)
        Con.closeCnt()


    def importReply(self,art):
        con = DBConnect()
        for li in art.replyList:
            flag = con.get_date("select id from reply where id = '%s' " %li.id)
            if flag is None:
                li.fn = 0 if li.fn == "" else li.fn
                li.floor_num = -1 if li.floor_num == "" else li.floor_num
                li.date = art.date if li.date == "" or li.date == None  else li.date
                # print(li.user.img_path)
                # print(li.user.username)
                if li.fn==0:
                    try:
                        userFlag = li.user.checkUserByUserName(li.user.username)
                        if userFlag is None:
                            con.update_info("insert into users(img_path,username) values ('%s','%s') " % (
                            li.user.img_path, li.user.username))
                        sql = "insert into reply(id,content,author,date,floor_num,fn,article_id)values('%s','%s','%s','%s','%s','%s','%s')"%(
                            li.id, li.content, li.author,li.date,li.floor_num, li.fn, art.id)
                        con.update_info(sql)
                    # print(sql)
                    except IntegrityError:
                        print("Duplicate entry '123197159870' for key 'PRIMARY'")
                else:
                    try:
                        userFlag = li.user.checkUserByUserName(li.user.username)
                        if userFlag is None:
                            con.update_info("insert into users(img_path,username) values ('%s','%s') " % (
                                li.user.img_path, li.user.username))
                        sql = "insert into reply_lzz(id,content,author,date,floor_num,fn,article_id)values('%s','%s','%s','%s','%s','%s','%s')" % (
                            li.id, li.content, li.author, li.date, li.floor_num, li.fn, art.id)
                        con.update_info(sql)
                    except IntegrityError:
                        print("Duplicate entry '123197159870' for key 'PRIMARY'")
        con.closeCnt()




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