# coding:utf-8
import requests
from crawBaidu.craw.download.constants import get_headers
from crawBaidu.craw.dao.proxy import Proxies
import requests.exceptions as exc
import time

class Downloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(get_headers)

    def reqGet(self, url, proxy = None,Referer=None,Origin=None):
        Referer and self.session.headers.update({'Referer': Referer})
        Origin and self.session.headers.update({'Origin': Origin})
        proxy and self.session.proxies.update(proxy.prox)
        timeout = 30
        try:
            return self.session.get(url, timeout=timeout)
        except exc.ProxyError as e:
            flag = True
        except exc.ConnectTimeout as e:
            return self.reqGet(url, proxy=Proxies(db='cn'))
        except exc.ConnectionError as e:
            print(e)
            flag = True
        except exc.ReadTimeout as e:
            print(e)
            flag = True
        # except exc.ChunkedEncodingError as e:
        #     return self.reqGet(url, proxy=Proxies(db='cn'))
        if flag and proxy is not None:
            print("当前代理", proxy, "不可用,0.1s后尝试使用其他代理连接,此代理将会被删除.")
            if proxy.testProxy() is not True:proxy.deleteProxy()
            time.sleep(0.1)
            return self.reqGet(url, proxy=Proxies(db='cn'))

# if __name__ == '__main__':
#     url = 'https://tieba.baidu.com/mo/q/m?kz=5975305662&has_url_param=0&is_ajax=1&post_type=normal&_t=1544507042457&pn=30&is_ajax=1&fid=1185508'
#     down = Downloader()
#     req = down.reqGet(url, proxy=Proxies(db='cn'))
#     print(req.text)