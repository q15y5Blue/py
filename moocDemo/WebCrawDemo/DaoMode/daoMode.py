'''
Created on 2017年7月7日

@author: q15y5Blue
'''
#coding:utf8
from demo.entity.news import News
from WebCrawDemo.until.Connection import connectionClazz

class DaoMode(object):
    
    def updateNews(self,news=News()):
        try:
            connect=connectionClazz.connection
            with connect.cursor() as cursors:
                sql="insert into news(content,url,author,src,tim) values(%s,%s,%s,%s,%s)"
                print("执行了sql语句:",sql)
                cursors.execute(sql,(news.content,news.url,news.authors,news.src,news.tim))
                connect.commit()
        finally:
            cursors.close()
            print("关闭游标")