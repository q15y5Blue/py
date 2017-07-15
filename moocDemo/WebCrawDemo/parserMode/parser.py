'''
Created on 2017年7月7日

@author: q15y5Blue
'''
import re
from bs4 import BeautifulSoup
from datetime import datetime
from WebCrawDemo.entity.news import News

class Parser(object):
    
    #根据url获取news对象的回复
    #http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/CP5TJASH0001875P/comments/newList?offset=%s&limit=30&headLimit=1&tailLimit=2&ibc=newspc&_=1499993966.807994
    def _getNewsDetails(self,url):
        if url is  None :
            return
        
        
    #根据url解析news对象
    def _getNewsByHTML(self,html_doc,url):  
        soup=BeautifulSoup(html_doc,"html.parser")   #response 解析
        news=News()
        #soup=html_doc
        #title get  
        #news.title(soup.h1.string)
        news.title=soup.h1.string
        
        #content get
        listAllPage=soup.find_all('p')
        contentStr=' '.join('%s' %it for it in listAllPage)
        regex="""<p>.*?</p>"""
        matches = re.findall(regex,contentStr)
        contentStr=' '.join('%s' %it for it in matches)
        news.content=contentStr
        #<p><!-- AD200x300_2 -->
        ####################################################################BUG
#         startNum=0
#         endNum=0
#         for st in listAllPage :
#             if st.prettify().__contains__(starStr) :
#                 startNum=listAllPage.index(st)
#                 del listAllPage[0:startNum]
#                 if st.prettify().__contains__(endStr):
#                     endNum=listAllPage.index(st)
#                     del listAllPage[endNum:-1]
#                     content=" ".join('%s' %it for it in listAllPage)
#                     news.content=content
        
        #author and time
        author=soup.find("div",class_="post_time_source")
        ti=re.search("\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d",author.__str__())
        datetimeObj=datetime.strptime(ti.group(0),"%Y-%m-%d %H:%M:%S")
        #news.tim(datetimeObj)
        news.tim=datetimeObj
    
        #author get
        
        authorStr=re.search("(?<=>).*?(?=</a>)",author.__str__()).group(0)
        #news.authors(authorStr)
        news.authors=authorStr
        #news.url(url)
        news.url=url
        #news.src("网易新闻")
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
    
    #根据url获取新闻评论
    def parseDetails(self,url):
        return self._getNewsDetails(url)
    
        
