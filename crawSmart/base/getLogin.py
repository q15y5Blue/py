# -*- coding: utf-8 -*-
import requests
import datetime
from .constant import req_header,constant,url_login


class BaseAction(object):
    def loginAction(self):
        self.prepareSession()

    def prepareSession(self):
        self.session = requests.Session()
        self.session.headers.update(req_header)
        self.getUrl = url_login


#first
def first_step():
    rul_img_show = """https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=2&l=M&s=3&d=72&v=4&t=0.686312473063923&daid=164&pt_3rd_aid=0
    """
    url_img_login = """https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fweb2.qq.com%2Fproxy.html&
    ptqrtoken=409413263&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-1536038493274&js_ver=10278&js_type=1&
    login_sig=yKVGvBluB6ZEisSjYwuyL0w2fumpc7hdStnIonePXiJGMWKretRujSj0N9Qb-Fi-&
    pt_uistyle=40&aid=501004106&daid=164&mibao_css=m_webqq&
    """

# 获取登录二维码
def get_url_img(url):
    r = requests.get(url, headers=req_header)
    results = r.content
    filename = url.split('/')[-1]+".png"
    with open(filename, 'wb') as f:
        f.write(results)


# this is a problems this is a picture linear function
if __name__ == "__main__":
    url = "https://ssl.ptlogin2.qq.com/ptqrshow"
    get_url_img(url)

