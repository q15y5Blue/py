'''
Created on 2017年7月7日

@author: q15y5Blue
'''
import re
from _datetime import datetime

class UrlManager(object):
    
    #初始化url，并能做到去重效果
    def __init__(self):
        self.newUrl=set()
        self.oldUrl=set()

    #添加新的url
    def addNewUrl(self,url):
        if url is None:
            return 
        if url not in self.oldUrl and url not in self.newUrl:
            self.newUrl.add(url)
    
    def hasNewUrl(self):
        return len(self.newUrl)!=0
    
    #获取一个新的url
    def getNewUrl(self):
        url=self.newUrl.pop()
        self.oldUrl.add(url)
        return url

    
    def addUrlList(self,urlList):
        if urlList is None or len(urlList)==0:
            return
        for url in urlList:
            self.addNewUrl(url)
    
    #url转换
    #http://news.163.com/17/0711/09/CP29MMOJ0001899O.html
    def convertUrl(self,url):
        replyUrl="http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/%s/comments/newList?offset=30&limit=30&headLimit=1&tailLimit=2&ibc=newspc&_=%s"
        newIds=re.search(""".{16}(?=.html)""", url)
        replyUrl=replyUrl%(newIds.group(0),datetime.timestamp(datetime.today()))
        return replyUrl