#coding:utf8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from demo.entity.news import News
from datetime import datetime
from demo.execute.getUrls import getUrls
from demo.dao import NewsDao
#在beautifulsoup中prettify()才是获取字符串的方法
#根据Url获取News对象
#from demo.execute.getUrls import getUrls
#url=url= "http://news.163.com/rank/"
#list = getUrls(url)
#http://news.163.com/17/0629/01/CO2I1NJR00018AOP.html
#根据url获取详细的news对象
url ="http://news.163.com/17/0629/01/CO2I1NJR00018AOP.html";

#根据一个url地址获取详细的news对象
def getNewsByUrl(url):  
    news=News()
    #打开一个文本
    resp=urlopen(url).read().decode("gbk")
    soup=BeautifulSoup(resp,"html.parser")
    
    #title get  
    news.title=soup.h1.string
    
    #content get
    listAllPage=soup.findAll('p')
    starStr="""f_center"""
    num=0
    for st in listAllPage :
        if st.prettify().__contains__(starStr) :
            num=listAllPage.index(st)
    del listAllPage[0:num]
    del listAllPage[-6:-1]
    content=" ".join('%s' %it for it in listAllPage)
    news.content=content

    #author and time
    author=soup.find("div",class_="post_time_source")
    ti=re.search("\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d",author.__str__())
    datetimeObj=datetime.strptime(ti.group(0),"%Y-%m-%d %H:%M:%S")
    news.tim=datetimeObj
    #datetimeStamp=datetime.timestamp(datetimeObj)
    #news.tim=datetimeStamp#时间get datetimeStamp 是float类型
    print(datetimeObj.__str__())#2017-06-29 01:58:01
    print(news.tim)#1498672681.0
    
    #author get
    news._authors=re.search("(?<=>).*?(?=</a>)",author.__str__()).group(0)
    news.url=url
    news.src="网易新闻"
    print("爬到了一个新闻  标题为:",news.title)
    return news

def testANews():
    newt=getNewsByUrl(url)
    NewsDao.updateNewsObj(newt)

def testSelectAllNews():
    return NewsDao.selectAllNews()
