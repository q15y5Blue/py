'''
Created on 2017年7月7日

@author: q15y5Blue
'''
import re
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request

from WebCrawDemo.entity.news import News

class Parser(object):
    
    def _getNewsByHTML(self,html_doc,url):  
        soup=BeautifulSoup(html_doc,"html.parser")   #response 解析
        news=News()
        #soup=html_doc
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
    
        #author get
        news._authors=re.search("(?<=>).*?(?=</a>)",author.__str__()).group(0)
        news.url=url
        news.src="网易新闻"
        print("爬到了一个新闻  标题为:",news.title)
        return news
    
    #根据html内容解析出url 并以list返回
    def _parserURL(self,html_doc):
        soup=BeautifulSoup(html_doc,"html.parser")   #response 解析
        listUrls = soup.findAll("a",href=re.compile("http://news\.163\.com"))
        lists=[]
        for url in listUrls :
            #正则匹配
            if re.search("\d+\/\d+\/\d+",url["href"]) :
                lists.append(url["href"])
        return lists
    
    
    def parseUrls(self,html_doc):
        return self._parserURL(html_doc)

    def parseData(self,html_doc,url):
        return self._getNewsByHTML(html_doc,url)
