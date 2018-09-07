# -*- coding: utf-8 -*-
import random as ra
import requests
import sys, os
import time


from crawSmart.base.constant import req_header, constant, url_login, cookie


class BaseAction(object):
    def loginAction(self,conf):
        self.prepareSession()
        self.waitForAuth(conf)

    def prepareSession(self):
        self.session = requests.Session()
        self.session.headers.update(req_header)
        self.session.cookies.update(cookie)
        self.getUrl(url_login)#第一个url
        self.getAuthStatus()
        self.session.cookies.pop("qrsig")


    # 检测二维码扫描状态的
    def getAuthStatus(self):
        qrsig = bknHash(self.session.cookies['qrsig'], init_str=0)
        print(qrsig)
        random = repr(ra.random() * 900000 + 1000000)
        url = "https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fweb2.qq.com%2Fproxy.html&"\
                  "ptqrtoken="+str(qrsig)+\
                  "&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-"+random+"&js_ver=10278&js_type=1&"\
                  "sig=yKVGvBluB6ZEisSjYwuyL0w2fumpc7hdStnIonePXiJGMWKretRujSj0N9Qb-Fi-&"\
                  "pt_uistyle=40&aid=501004106&daid=164&mibao_css=m_webqq&"
        referer = (url_login)# 1347769.2213467043
        print(url_login)
        result = self.getUrl(url_login, referer=referer).content.decode("utf8")
        print(result)
        # ptuiCB('65','0','','0','二维码已失效。(988817572)', '')
        # 65:过期    0:扫描成功    67:二维码已经扫描,等待确认        第一个参数是状态 第三个参数是跳转的连接
        return result

    #
    def getUrl(self, url, data=None, referer=None, origin=None):
        referer and self.session.headers.update({'Referer': referer})
        origin and self.session.headers.update({'Origin': origin})
        timeout = 30 if url != 'http://w.qq.com/' else 120  # 这里url已经不存在了######################question1111

        try:
            if data is None:
                return self.session.get(url, timeout=timeout)
            else:
                return self.session.get(url, data=data, timeout=timeout)
        except (requests.exceptions.SSLError, AttributeError):
            if self.session.verify:
                time.sleep(5)
                print("无法和腾讯服务器建立连接,5秒后将使用非私密连接和腾讯服务器建立连接") # System.out.println("yy");
                try:
                    time.sleep(5)
                except KeyboardInterrupt:
                    sys.exit(0)
                self.session.verify=False
                return self.getUrl(url, data, referer, origin)
            else:
                raise

# QrcodeManager
    def waitForAuth(self, conf):
        pass


#first
def first_step():
    rul_img_show = """https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=2&l=M&s=3&d=72&v=4&t=0.686312473063923&daid=164&pt_3rd_aid=0
    """
     # url_login = """https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fweb2.qq.com%2Fproxy.html&
            #    ptqrtoken=409413263
            #    &ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-1536038493274&js_ver=10278&js_type=1&
            #    sig=yKVGvBluB6ZEisSjYwuyL0w2fumpc7hdStnIonePXiJGMWKretRujSj0N9Qb-Fi-&
            #    pt_uistyle=40&aid=501004106&daid=164&mibao_css=m_webqq&
            #    """

# 获取登录二维码
def get_url_img(url):
    r = requests.get(url, headers=req_header)
    results = r.content
    filename = url.split('/')[-1]+".png"
    with open(filename, 'wb') as f:
        f.write(results)


def bknHash(skey, init_str=5381):
    hash_str = init_str
    for i in skey:
        hash_str += (hash_str << 5) + ord(i)
    hash_str = int(hash_str & 2147483647)
    return hash_str

def qHash(x, K):
    N = [0] * 4
    for T in range(len(K)):
        N[T%4] ^= ord(K[T])

    U, V = 'ECOK', [0] * 4
    V[0] = ((x >> 24) & 255) ^ ord(U[0])
    V[1] = ((x >> 16) & 255) ^ ord(U[1])
    V[2] = ((x >>  8) & 255) ^ ord(U[2])
    V[3] = ((x >>  0) & 255) ^ ord(U[3])

    U1 = [0] * 8
    for T in range(8):
        U1[T] = N[T >> 1] if T % 2 == 0 else V[T >> 1]

    N1, V1 = '0123456789ABCDEF', ''
    for aU1 in U1:
        V1 += N1[((aU1 >> 4) & 15)]
        V1 += N1[((aU1 >> 0) & 15)]

    return V1


if __name__ == "__main__":
    ba = BaseAction()
    ba.loginAction(conf="conf")
    # print(url)