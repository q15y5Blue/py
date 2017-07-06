#coding:utf8
from WebCraw.url_manager import url_manager
from WebCraw.html_downloader import html_downloader
from WebCraw.html_parser import html_parser
from WebCraw.html_outputer import html_outputer


class SpiderMain(object):
    #初始化
    def __init__(self):
        self.urls=url_manager.UrlManager()              #url管理器
        self.downloader=html_downloader.HtmlDownloader()#网页下载器
        self.parser=html_parser.HtmlParser()             #网页解析器
        self.outputer=html_outputer.HtmlOutputer()      #网页输出
    
    #爬虫方法

    
    def craw(self, root_url):
        count = 1 #当前爬url数量
        
        self.urls.add_new_url(root_url)#添加新的url
        #遍历url
        while self.urls.has_new_url():
            try:
                new_url=self.urls.get_new_url()
                html_cont=self.downloader.download(new_url)
                new_urls,new_data=self.parser.parser(new_url,html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                
                print(count)
            except Exception as e:
                print("爬失败了，失败信息：",e)
     
        self.outputer.output_html()#输出收集好的数据

if __name__=="__main__":
    root_url="http://news.163.com/rank/"
    obj_spider=SpiderMain() #初始化
    obj_spider.craw(root_url)#爬