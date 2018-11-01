# -*- coding: utf-8 -*-
class reply(object):
    def __init__(self):
        self.id = ''
        self.content=''
        self.author=''
        self.date = ''
        self.floor_num = ''  # 楼层
        self.fn = self.floor_num  # 父级 fn等于楼层本身，这是个主回复帖。


class article(object):
    def __init__(self):
        self.id = ''
        self.title =''
        self.content = ''
        self.username = ''
        self.date = ''


class users(object):
    def __init__(self):
        self.id = ''
        self.username = ''
        self.showname = ''
        self.imgUlr = ''
