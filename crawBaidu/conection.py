# -*- coding: utf-8 -*-
# request基础
import requests
from crawBaidu import headers as heads
import requests.exceptions as exc
from crawBaidu.craw_proxy import NetProtocol
import time

class BaseSession(object):
    def __init__(self):
        self.prepareSession()
        self.proxy = {}

    def prepareSession(self):
        self.session = requests.Session()
        self.session.headers.update(heads.headers)

    # get request
    def reqGet(self, url, proxies=None, data=None, Referer=None, Origin=None):
        if proxies == True:print("正常尝试使用代理连接:",url)
        Referer and self.session.headers.update({'Referer': Referer})
        Origin and self.session.headers.update({'Origin': Origin})
        if proxies == True:
            self.proxy = NetProtocol()
            proxies = self.proxy
            # proxies = self.proxy
        else:
            proxies = NetProtocol(location='1')
            time.sleep(0.5)
        self.session.proxies.update(proxies.prox)
        timeout = 20
        flag = False
        try:
            return self.session.get(url, timeout=timeout, proxies=proxies.prox)
        except exc.ProxyError as e:
            flag = True
        except exc.ConnectTimeout as e:
            return self.reqGet(url, proxies=True)
        except exc.ConnectionError as e:
            print(e)
            flag = True
        except exc.ReadTimeout as e:
            print(e)
            flag = True
        except exc.ChunkedEncodingError as e:
            return self.reqGet(url, proxies=True)
        if flag and proxies is not None:
            print("当前代理", proxies, "不可用,0.1s后尝试使用其他代理连接,此代理将会被删除.")
            if proxies.testProxy() is not True:proxies.deleteProxy()
            time.sleep(0.1)
            # 这里碰到的小问题,如果直接调用self.reqGet方法,在上层调用reqGet会为空 所以return self....
            return self.reqGet(url, proxies=True)


# if __name__=="__main__":
#     ba = BaseSession()
#     re = ba.reqGet(url="http://icanhazip.com/", proxies=True)
#     print(re.text)
