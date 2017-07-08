'''
Created on 2017年7月7日

@author: q15y5Blue
'''

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
    
    
    
    
    
    



