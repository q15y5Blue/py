'''
Created on 2017年7月6日

@author: q15y5Blue
'''

#爬虫不仅要维护爬过的url，也要维护新的url
class UrlManager(object):
    
    def __init__(self):
        self.new_urls= set()
        self.old_urls= set()
    
    #添加待解析的url
    def add_new_url(self,url):
        if url is None:
            return 
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    #添加新urls，添加到url管理器中
    def add_new_urls(self,urls):
        if urls is None or len(urls) == 0:
            return 
        for url in urls :
            self.add_new_url(url)
        
    #是否有新的url
    def has_new_url(self):
        return len(self.new_urls)!=0
    
    #获取下一条url,待解析
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url
