'''
Created on 2017年7月7日

@author: q15y5Blue
'''
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime
from WebCrawDemo.entity.news import News
from urllib.request import urlopen
from WebCrawDemo.entity.reply import Reply

class Parser(object):
    
    #根据url获取news对象的回复，获取reply对象
    #http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/CP5TJASH0001875P/comments/newList?offset=%s&limit=30&headLimit=1&tailLimit=2&ibc=newspc&_=1499993966.807994
    def _getNewsDetails(self,html_data,url):
        if url is  None or html_data is None:
            return
        
        print("开始获取reply：…………………………………………………………………………………………")
        """……………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………"""
        ft=json.loads(html_data) #这个时候的s 是一个dict的类型
        listReply=set()
        for itsCommentsId in ft['comments']:
            reply=Reply()
            reply.against=ft['comments'][itsCommentsId]['against']
            reply.anonymous=ft['comments'][itsCommentsId]['anonymous']
            reply.buildlevel=ft['comments'][itsCommentsId]['buildLevel']
            reply.commentId=ft['comments'][itsCommentsId]['commentId']
            reply.content=ft['comments'][itsCommentsId]['content']
            reply.creatTime=ft['comments'][itsCommentsId]['createTime']
            reply.favCount=ft['comments'][itsCommentsId]['favCount']
            reply.ip=ft['comments'][itsCommentsId]['ip']
            reply.idDel=ft['comments'][itsCommentsId]['isDel']
            reply.postId=ft['comments'][itsCommentsId]['postId']
            reply.productKey=ft['comments'][itsCommentsId]['productKey']
            reply.shareCount=ft['comments'][itsCommentsId]['shareCount']
            reply.source=ft['comments'][itsCommentsId]['source']
            reply.unionState=ft['comments'][itsCommentsId]['unionState']
            reply.vote=ft['comments'][itsCommentsId]['vote']
            listReply.add(reply)
        
        #test
        for lt in listReply:
            print(lt.content)
        """……………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………………"""
            
    #根据url解析news对象,获取的是news新闻对象本身
    def _getNewsByHTML(self,html_doc,url):  
        soup=BeautifulSoup(html_doc,"html.parser")   #response 解析
        news=News()
        
        #title get  
        if(soup.h1.string is not None):
            news.title=soup.h1.string
        
        #content get
        listAllPage=soup.find_all('p')
        contentStr=' '.join('%s' %it for it in listAllPage)
        regex="""<p>.*?</p>"""
        matches = re.findall(regex,contentStr)
        contentStr=' '.join('%s' %it for it in matches)
        news.content=contentStr
        
        #time
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
    def parseDetails(self,html_data,url):
        return self._getNewsDetails(html_data,url)
    
def test():
    t=Parser()
    url="""http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/CP5TJASH0001875P/comments/newList?offset=%s&limit=30"""
    resp=urlopen(url).read()
    soup=BeautifulSoup(resp,"html.parser")
    t.parseDetails(soup.__str__(), url)
    
test()