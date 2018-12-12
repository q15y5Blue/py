# coding:utf-8
from crawBaidu.craw.download import DownLoader
from crawBaidu.craw.parser import Parser
from crawBaidu.craw.urlPool import UrlManage

class Execute:
    def __init__(self):
        self.urlObj = UrlManage()
        self.downloaderObj = DownLoader()
        self.parserObj = Parser()

    def execute(self, rootUrl):
        self.urlObj.add_new_url(rootUrl)
        count = 0
        while (self.urlObj.has_new_url()):
            count += 1
            new_url = self.urlObj.get_new_url()
            per = self.parserObj.parse_data_followings(new_url)  # 获取个人信息
            if per is not None:
                self.urlObj.add_new_url_list(per.get_following_str_to_list)
                self.urlObj.add_new_url_list(per.get_fans_str_to_list)
            print("次数呢:", count)

if __name__ == '__main__':
    root_url = "https://tieba.baidu.com/mo/q/m?kw=剑网3pn=0&lp=5024&lm=0&cid=0&has_url_param=0&pn=%s&is_ajax=1"% 0
    spider = Execute()
    spider.execute(root_url)