#encoding:utf8
import urllib.request as urllib2
class Downloader(object):
    
    def downloadHTML(self,url):
        #根据url下载新的网页内容
        request=urllib2.Request(url)
        request.add_header("user-agent", "Mozilla/5.0")
        response=urllib2.urlopen(request)
        if(response.getcode()==200):
            return response.read().decode("gbk")
        else :
            return None

