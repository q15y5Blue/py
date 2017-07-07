'''
Created on 2017年7月6日

@author: q15y5Blue
'''
import urllib.request as urllib2 

#网页下载器，只负责把网页下载下来
class HtmlDownloader(object):
    
    
    def download(self,url):
        if url is None :
            return None
        
        response = urllib2.urlopen(url)
        if (response.getcode()!=200):
            return None
        
        return response.read()

