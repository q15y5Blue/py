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
#http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/CP8865JC0001875P/comments/newList?offset=30&limit=30&headLimit=1&tailLimit=2&ibc=newspc&_=1499994675.72012
    def downloadReplyDate(self,url):
        request=urllib2.Request(url)
        request.add_header("user-agent", "Mozilla/5.0")
        response=urllib2.urlopen(request)
        if(response.getcode()==200):
            return response.read()
        else :
            return None