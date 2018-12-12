# -*- coding: utf-8 -*-
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

    def __str__(self):
        return "id:"+str(self.id)+'author:'+self.author+'date:'+self.date+'floor_num:'+str(self.floor_num)+str(self.fn)+'content:'+str(self.content)

class article(object):
    def __init__(self):
        self.id = ''
        self.title =''
        self.content = ''
        self.username = ''
        self.date = ''
        self.user = users()
        self.replyList = []


class users(object):
    def __init__(self, username=None, nick_name=None, img_path=None):
        self.id = ''
        self.username = username
        # self.nick_name = nick_name
        self.img_path = img_path

    def checkUserByUserName(self,username):
        from crawBaidu.db import DBConnect
        con = DBConnect()
        userFlag = con.get_date("select id,username from users where username = '%s' " % username)
        con.closeCnt()
        if userFlag is None:
            return None
        else:
            return userFlag[0]


