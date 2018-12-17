# -*- coding: utf-8 -*-
from crawBaidu.craw.dao.db import DBConnect
from mysql.connector.errors import IntegrityError
from crawBaidu.craw.dao.db import DBPool
po = DBPool().pool

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
        self.fn = 0 if self.fn =="" else self.fn
        self.floor_num = -1 if self.floor_num == "" else self.floor_num
        self.date = art if self.date == "" or self.date == None else self.date
        self.user.insertAuthor(con)
        if self.fn==0:
            try:
                sql = "insert into reply(id,content,author,date,floor_num,fn,article_id)values('%s','%s','%s','%s','%s','%s','%s')" % (
                    self.id, self.content, self.author, self.date, self.floor_num, self.fn, art.id)
                con.update_info(sql)
            except Exception:
                print("error: sql---:"+sql)
        else:
            try:
                sql = "insert into reply_lzz(id,content,author,date,floor_num,fn,article_id)values('%s','%s','%s','%s','%s','%s','%s')" % (
                    self.id, self.content, self.author, self.date, self.floor_num, self.fn, art.id)
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
        userFlag = self.user.checkUserByUserName(con)
        if userFlag is None:
            self.user.insertAuthor(con)
            userFlag = self.user.checkUserByUserName(con)
        sql = "insert into article(id,title,user_id,date,content)  values('%s','%s','%s','%s','%s') " % (
            self.id, self.title, userFlag, self.date, self.content)
        con.update_info(sql)
        con.closeCnt()
        self.importReplyList()
        print("insert a article: "+self.title)

    def importReplyList(self):
        # print(self.replyList)# error 为空
        for li in self.replyList:
            li.importReply(art=self)


class users(object):
    def __init__(self, username=None, nick_name=None, img_path=None):
        self.id = ''
        self.username = username
        self.img_path = img_path

    def insertAuthor(self, con=None):
        flag = 1
        if con is None:
            flag = 0
            con = DBConnect(pool=po)
        try:
            sql ="insert into users(img_path,username) values ('%s','%s') "%(self.img_path,self.username)
            con.update_info(sql)
        except:
            print("userExists")
        if flag == 0 : con.closeCnt()

    def checkUserByUserName(self,con = None):
        flag = 1
        if con is None:
            flag = 0
            con = DBConnect(pool=po)
        try:
            userFlag = con.get_date("select id,username from users where username = '%s' " % self.username)
        except Exception:
            print("checkUserByUserName Error")
        if flag == 0: con.closeCnt()
        if userFlag is None:
            return None
        else:
            return userFlag[0]

