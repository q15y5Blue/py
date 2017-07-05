#coding:utf8
#爬虫程序入口
from demo.execute.getUrls import getUrls
from demo.execute.getNews import getNewsByUrl
from demo.dao import NewsDao
from demo.until import pyMySqlDB
url="http://news.163.com/rank/"
list=getUrls(url)
print("url队列长度",list.__len__())
for l in list :
    newsObj = getNewsByUrl(l)
    NewsDao.updateNewsObj(newsObj)
connect=pyMySqlDB.connectionClazz.connection
connect.close()