#coding:utf8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

url= "http://news.163.com/rank/"

#getUrls
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

#######################################################################################
#for urls in getUrsl(url) :                                                           #   
#    if re.search("\d+\/\d+\/\d+",urls["href"]) :                                     #
#        print(urls.get_text(),"--------",urls["href"])                               #
#######################################################################################
print(getUrls(url))    
    