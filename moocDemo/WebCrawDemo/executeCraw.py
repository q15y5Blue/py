#coding:utf8
from WebCrawDemo.urlManagerMode import urlManager
from WebCrawDemo.downloadMode   import downloader
from WebCrawDemo.parserMode     import parser
from WebCrawDemo.DaoMode        import daoMode

class CrawExecute(object):
    def __init__(self):
        self.urlObj=urlManager.UrlManager()             #urlManager
        self.downloadObj=downloader.Downloader()        #downloader
        self.parserObj=parser.Parser()                  #解析
        self.daoModeObj=daoMode.DaoMode()               #数据处理

    def craw(self,rootUrl):
        self.urlObj.addNewUrl(rootUrl)          #向url管理器中添加新的url
        
        #判断是否有新的url
        count=0
        while self.urlObj.hasNewUrl() :
            #对网页列表的爬虫
            if(count==0):
                newUrl=self.urlObj.getNewUrl()
                html_doc=self.downloadObj.downloadHTML(newUrl)
                urlList=self.parserObj.parseUrls(html_doc)
                self.urlObj.addUrlList(urlList)
            else:    
                #对新闻的爬虫
                newUrl=self.urlObj.getNewUrl()
                html_doc=self.downloadObj.downloadHTML(newUrl) #根据url下载网页内容
                newst=self.parserObj.parseData(html_doc,newUrl)#根据网页内容和url解析新闻
                reply=self.parserObj.parseDetails(newst.url)#####news added
                self.daoModeObj.updateNews(newst)      
                self.daoModeObj.updateReply(reply)   #####news added    
            count+=1
        print("爬虫程序结束，爬取新闻数量：",count)
        
#main方法 
if __name__=="__main__":
    rootUrl="http://news.163.com/rank/"
    spider=CrawExecute()
    spider.craw(rootUrl)