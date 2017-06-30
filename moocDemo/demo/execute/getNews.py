#coding:utf8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import codecs

#根据Url获取News对象
#from demo.execute.getUrls import getUrls
#url=url= "http://news.163.com/rank/"
#list = getUrls(url)
#http://news.163.com/17/0629/01/CO2I1NJR00018AOP.html
#根据url获取详细的news对象

url ="http://news.163.com/17/0629/01/CO2I1NJR00018AOP.html";
def getNewsByUrl(url):  
    resp=urlopen(url).read().decode("gbk")
    soup=BeautifulSoup(resp,"html.parser")
    fil1=codecs.open(r"D:\test\test.html","r",'utf-8')
    fil2=codecs.open(r"D:\test\cache.html","w","utf-8")
    print(fil1.read())
    #fil2.write(fil1.read())
    fil1.close()
    fil2.close()
    
    #listUrls = soup.findAll()
    
getNewsByUrl(url)