# -*- coding: utf-8 -*-
# request基础
import requests
from crawBaidu import headers as heads
from crawBaidu.craw_proxy import *

class BaseSession(object):
    def __init__(self):
        self.prepareSession()

    def prepareSession(self):
        self.session = requests.Session()
        self.session.headers.update(heads.headers)

    # get request
    def reqGet(self, url, proxies=None, data=None, Referer=None, Origin=None):
        Referer and self.session.headers.update({'Referer':Referer})
        Origin and self.session.headers.update({'Origin':Origin})
        proxies and self.session.proxies.update(proxies.prox)
        timeout = 10
        try:
            return self.session.get(url, timeout=timeout, proxies=proxies.prox)
        except requests.exceptions.ProxyError or requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
            print("这个代理有问题,可以尝试下一个")


# if __name__=="__main__":
#     ba = BaseSession()
#     print(ba.reqGet("http://www.runoob.com"))