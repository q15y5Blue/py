#coding:utf8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from demo.entity.news import News
from demo.entity import news
import time
#在beautifulsoup中prettify()才是获取字符串的方法
#根据Url获取News对象
#from demo.execute.getUrls import getUrls
#url=url= "http://news.163.com/rank/"
#list = getUrls(url)
#http://news.163.com/17/0629/01/CO2I1NJR00018AOP.html
#根据url获取详细的news对象
url ="http://news.163.com/17/0629/01/CO2I1NJR00018AOP.html";
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
    for st in listAllPage :
        if st.prettify().__contains__(starStr) :
            num=listAllPage.index(st)
    del listAllPage[0:num]
    del listAllPage[-6:-1]
    content=" ".join('%s' %it for it in listAllPage)
    news.content=content

    #author
    #author=soup.div['class="post_time_source']
    author=soup.find("div",class_="post_time_source")
    print(author.__str__())
    tim=re.search("\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d",author.__str__())
    news.time=tim.group(0)
    
#getNewsByUrl(url)



