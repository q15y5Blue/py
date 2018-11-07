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
        self.child = []

    def __str__(self):
        return "id:"+str(self.id)+'author:'+self.author+'date:'+self.date+'floor_num:'+str(self.floor_num)+str(self.fn)+'content:'+str(self.content)

class article(object):
    def __init__(self):
        self.id = ''
        self.title =''
        self.content = ''
        self.username = ''
        self.date = ''
        self.replyList = []


class users(object):
    def __init__(self):
        self.id = ''
        self.username = ''
        self.showname = ''
        self.imgUlr = ''
