# coding:utf-8
from crawBaidu.craw.download.DownLoader import Downloader
from crawBaidu.craw.parser.Parser import Parser
from crawBaidu.craw.urlPool.UrlManage import UrlManage
from crawBaidu.craw.dao.entity import article


class Execute(object):
    def __init__(self):
        self.urlObj = UrlManage()
        self.downloaderObj = Downloader()
        self.parserObj = Parser()
        self.articleObj = article()

    def execute(self, rootUrl):
        self.urlObj.add_new_url(rootUrl)
        count = 0
        while (self.urlObj.has_new_url()):
            count += 1
            new_url = self.urlObj.get_new_url()
            self.parserObj.parserArticleList(new_url)
            # articleObj.importArticle()
            print("次数呢:", count)


if __name__ == '__main__':
    root_url = "https://tieba.baidu.com/mo/q/m?kw=剑网3&pn=%d&lm=0&cid=0&has_url_param=0&is_ajax=1" % 0
    spider = Execute()
    spider.execute(root_url)