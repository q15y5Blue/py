'''
Created on 2017年7月7日

@author: q15y5Blue
'''
#coding:utf8
from WebCrawDemo.until.Connection import connectionClazz
from WebCrawDemo.entity.news import News

class DaoMode(object):
    
    def updateNews(self,news=News()):
        print(news)
        try:
            connect=connectionClazz.connection
            with connect.cursor() as cursors:
                sql="insert into news(title,content,url,author,src,tim) values(%s,%s,%s,%s,%s,%s)"
                print("执行了sql语句:",sql)
                cursors.execute(sql,(news.title,news.content,news.url,news.authors,news.src,news.tim))
                connect.commit()
        finally:
            cursors.close()
            print("关闭游标")
    
    def updateReply(self,reply):
        pass
    
    
