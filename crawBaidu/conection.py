# -*- coding: utf-8 -*-
# request基础
import requests
from crawBaidu import headers as heads
import requests.exceptions as exc
from crawBaidu.craw_proxy import *

class BaseSession(object):
    def __init__(self):
        self.prepareSession()

    def prepareSession(self):
        self.session = requests.Session()
        self.session.headers.update(heads.headers)

    # get request
    def reqGet(self, url, proxies=None, data=None, Referer=None, Origin=None):
        Referer and self.session.headers.update({'Referer': Referer})
        Origin and self.session.headers.update({'Origin': Origin})
        proxies= proxies or NetProtocol(location=None, port=None)
        self.session.proxies.update(proxies.prox)
        timeout = 20
        flag = False
        try:
            return self.session.get(url, timeout=timeout, proxies=proxies.prox)
        except exc.ProxyError:
            flag = True
        except exc.ConnectTimeout:
            flag = True
        except exc.ConnectionError:
            flag = True
        except exc.ReadTimeout:
            flag = True
        if flag and proxies is not None:
            print("当前代理", proxies, "不可用,0.1s后尝试使用其他代理连接,此代理将会被删除.")
            proxies.deleteProxy()
            time.sleep(0.1)
            # 这里碰到的小问题,如果直接调用self.reqGet方法,在上层调用reqGet会为空 所以return self....
            return self.reqGet(url, proxies=NetProtocol())


# if __name__=="__main__":
    # ba = BaseSession()
    # re = ba.reqGet(url="http://icanhazip.com/", proxies=NetProtocol())
