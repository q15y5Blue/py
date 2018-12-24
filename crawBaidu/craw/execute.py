# coding:utf-8
import sys,os
pwd = os.getcwd()
grader_father = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
sys.path.extend([grader_father])
from crawBaidu.craw.download.DownLoader import Downloader
from crawBaidu.craw.parser.Parser import Parser
from crawBaidu.craw.urlPool.UrlManage import UrlManage

# reply date 有时会为空?
class Execute(object):
    def __init__(self):
        self.urlObj = UrlManage()
        self.downloaderObj = Downloader()
        self.parserObj = Parser()

    def execute(self, rootUrl):
        page = 0
        for page in (50):
            url = root_url % page
            self.urlObj.add_new_url(url)
        # self.urlObj.add_new_url(rootUrl)
        count = 0
        while self.urlObj.has_new_url():
            count += 1
            new_url = self.urlObj.get_new_url()
            self.parserObj.parserArticleList(new_url)
            print("次数呢:", count)
            if count < 100:
                self.urlObj.add_new_url(rootUrl)
            else:
                break


if __name__ == '__main__':
    root_url = "https://tieba.baidu.com/mo/q/m?kw=剑网3&pn=%d&lm=0&cid=0&has_url_param=0&is_ajax=1"
    spider = Execute()
    spider.execute(root_url)
    # print(path)
