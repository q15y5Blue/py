# coding:utf-8
import sys, os
pwd = os.getcwd()
grader_father = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
sys.path.extend([grader_father])

from crawBaidu.craw.download.DownLoader import Downloader
from crawBaidu.craw.parser.Parser import Parser
from crawBaidu.craw.urlPool.UrlManage import UrlManage
from crawBaidu.craw.util.log import *

# reply date 有时会为空?
class Execute(object):
    def __init__(self):
        self.urlObj = UrlManage()
        self.downloaderObj = Downloader()
        self.parserObj = Parser()

    def execute(self):
        count = 0
        while self.urlObj.has_new_url():
            count += 1
            new_url = self.urlObj.get_new_url()
            self.parserObj.parserArticleList(new_url)
            info(count)


if __name__ == '__main__':
    spider = Execute()
    url = "https://tieba.baidu.com/mo/q/m?kw=%s&lm=0&cid=0&has_url_param=0&is_ajax=1"
    key1 = '剑网3'
    key2 = '双梦镇'
    key3 = '长歌门'
    # sys.argv.append(key1)
    # sys.argv.append(key2)
    # sys.argv.append(key3)
    urlList = []
    for key in sys.argv[1:]:
        urlList.append(url % key)
    spider.urlObj.add_new_url_list(url_list=urlList, pageSize=5)
    spider.execute()
