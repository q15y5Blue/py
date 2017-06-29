#coding:utf8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from demo.dao import urlsDao

url= "http://news.163.com/rank/"

#获取新闻url
def getUrls(url):
    resp = urlopen(url).read().decode("gbk") #get response
    soup=BeautifulSoup(resp,"html.parser")   #response 解析
    #http://news.163.com/17/0627/19/CNV9UA1S0001899N.html []
    #找到所有的<a>超链接标签</a>
    listUrls = soup.findAll("a",href=re.compile("http://news\.163\.com"))
    lists=[]
    for url in listUrls :
        #正则匹配
        if re.search("\d+\/\d+\/\d+",url["href"]) :
            lists.append(url["href"])
    return lists

############################################################################
#把获取到的url存到数据库里去
#def updateUrlTable(urlName,urlHref):
#    urlsDao.updateUrls(urlName,urlHref)
   

