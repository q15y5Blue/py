# -*- coding: utf-8 -*-
from crawBaidu.craw.dao.db import DBConnect
from crawBaidu.craw.dao.constant import *
from mysql.connector.errors import IntegrityError
from crawBaidu.craw.dao.db import DBPool
from crawBaidu.craw.util.log import *
po = DBPool().pool
# userList = NameList(200)

class reply(object):
    def __init__(self):
        self.id = ''
        self.content=''
        self.author=''
        self.date = ''
        self.floor_num = ''  # 楼层
        self.fn = ''  # 父级 fn等于楼层本身，这是个主回复帖。
        self.articleId = ''
        self.user = users()
        # self.child = []

    def importReply(self, art):
        con = DBConnect(pool=po)
        self.fn = 0 if self.fn == "" else self.fn
        self.floor_num = -1 if self.floor_num == "" else self.floor_num
        self.date = art if self.date == "" or self.date == None else self.date
        self.user.insertAuthor(con)
        user = self.user.checkUserByUserName(con)
        # userList.addList(self.user)
        if self.fn==0:
            try:
                sql = "insert into reply(id,content,author,date,floor_num,fn,article_id,author_id)values('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    self.id, self.content, self.author, self.date, self.floor_num, self.fn, art.id, user.id)
                con.update_info(sql)
            except Exception:
                print("error: sql---:"+sql)
        else:
            try:
                sql = "insert into reply_lzz(id,content,author,date,floor_num,fn,article_id,user_id)values('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    self.id, self.content, self.author, self.date, self.floor_num, self.fn, art.id, user.id)
                con.update_info(sql)
            except Exception:
                print("error: sql---:"+sql)
        con.closeCnt()

    def __str__(self):
        return "id:"+str(self.id)+'author:'+self.author+'date:'+self.date+'floor_num:'+str(self.floor_num)+str(self.fn)+'content:'+str(self.content)


class article(object):
    def __init__(self):
        self.id = ''
        self.title = ''
        self.content = ''
        self.username = ''
        self.date = ''
        self.user = users()
        self.replyList = [reply()]

    def checkArticleExists(self):
        con = DBConnect(pool=po)
        try:
            flag = con.get_date("select id from article where id = '%s' " % self.id)
        except Exception:
            print("查询出错")
        con.closeCnt()
        return flag

    def importArticle(self):
        con = DBConnect(pool=po)
        # userFlag = self.user.checkUserByUserName(con)
        self.user.insertAuthor(con)
        user = self.user.checkUserByUserName(con)
        sql = "insert into article(id,title,user_id,date,content)  values('%s','%s','%s','%s','%s') " % (
            self.id, self.title, user.id, self.date, self.content)
        con.update_info(sql)
        con.closeCnt()
        self.importReplyList()
        print("insert a article: "+self.title)

    def importReplyList(self):
        # print(self.replyList) # error 为空
        if self.replyList is None:
            error("self.replyList is None")
            return
        for li in self.replyList:
            li.importReply(art=self)


class users(object):
    def __init__(self,id= None, username=None, nick_name=None, img_path=None):
        self.id = id
        self.username = username
        self.img_path = img_path

    def __eq__(self, other):
        if isinstance(other, users):
            return self.username == other.username and self.id == other.id

    def insertAuthor(self, con=None):
        if con is None:
            flag = 0
            con = DBConnect(pool=po)
        sql ="insert into users(img_path, username) values ('%s','%s') "%(self.img_path, self.username)
        flag = con.update_info(sql)
        if flag == 0 : con.closeCnt()

    # getUserId
    def checkUserByUserName(self,con = None):
        flag = 1
        if con is None:
            flag = 0
            con = DBConnect(pool=po)
        try:
            userFlag = con.get_date("select id,username,img_path from users where username = '%s' " % self.username)
            if flag == 0: con.closeCnt()
            if userFlag is None:
                return None
            else:
                self.id = userFlag[0]
                return self
        except Exception:
            print("checkUserByUserName Error")
