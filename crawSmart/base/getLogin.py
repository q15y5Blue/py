# -*- coding: utf-8 -*-
import random
import requests
import sys, os
import time
import json
from crawSmart.base import log
from crawSmart.base.constant import req_header, url_login, cookie
from crawSmart.base.qrManager import QrcodeManager

class BaseAction(object):
    def loginAction(self,conf):
        self.prepareSession() # cookies Set
        self.waitForAuth(conf)
        self.getPtwebqq()
        self.getVFwebqq()
        self.getUinandPsessionId()

    def prepareSession(self):
        self.clientid = 53999199
        self.psessionid = 1541574616852
        self.session = requests.Session()#session
        self.session.headers.update(req_header)#header
        self.getUrl(url_login)#第一个ui
        self.session.cookies.update(cookie)
        self.getQRCodeStatus()
        self.session.cookies.pop("qrsig")


    # 获取二维码状态的 getAuthStatus
    def getQRCodeStatus(self):
        qrsig = str(bknHash(self.session.cookies['qrsig'], init_str=0))
        url ="https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fweb2.qq.com%2Fproxy.html&ptqrtoken="+qrsig+"&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&" \
            "action=0-0-"+repr(random.random() * 900000 + 1000000)+"&js_ver=10282&js_type=1&login_sig=SAfRAEE2YNI5GVLErMLUfSbg-tMfbZjGaVugh*VmdmF36QFkkxSFjsBGMwibqYAJ&pt_uistyle=40&aid=501004106&daid=164&mibao_css=m_webqq&"
        referer = (url_login)
        result = self.getUrl(url, referer=referer).content.decode("utf8")
        return result


    #
    def getUrl(self, url, data=None, referer=None, origin=None):
        referer and self.session.headers.update({'Referer': referer})
        origin and self.session.headers.update({'Origin': origin})
        timeout = 30 if url != 'https://d1.web2.qq.com/channel/poll2' else 120  # 这里url已经不存在了######################question1111
        try:
            if data is None:
                return self.session.get(url, timeout=timeout)
            else:
                return self.session.post(url, data=data, timeout=timeout)
        except (requests.exceptions.SSLError, AttributeError):
            if self.session.verify:
                time.sleep(5)
                print("无法和腾讯服务器建立连接,5秒后将使用非私密连接和腾讯服务器建立连接")
                try:
                    time.sleep(5)
                except KeyboardInterrupt:
                    sys.exit(0)
                self.session.verify=False
                return self.getUrl(url, data, referer, origin)
            else:
                raise

    # 获取登录二维码
    def getQRCodeImg(self):
        url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=2&l=M&s=3&d=72&v=4&t='\
                        +repr(random.random())+\
                       "&daid=164&pt_3rd_aid=0"
        qrcode = self.getUrl(url).content
        with open("../img/qrCode.png", 'wb') as f:
            f.write(qrcode)
        # return qrcode

    # 获取二维码扫描状态的
    def waitForAuth(self, conf):# getQrcode
        self.getQRCodeImg()
        qrcodeShow = QrcodeManager()
        qrcodeShow.showImg()
        try:
            x, y = 1, 1
            while True:
                time.sleep(3)
                qrStatus = self.getQRCodeStatus()
                if '二维码未失效' in qrStatus:
                    if x:
                        log.info('等待二维码扫描及授权...')
                        x = 0
                elif '二维码认证中' in qrStatus:
                    if y:
                        print('二维码已扫描，等待授权...')
                        y = 0
                elif '二维码已失效' in qrStatus:
                    log.warn('二维码已失效, 重新获取二维码')
                    self.getQRCodeImg()
                    qrcodeShow = QrcodeManager()
                    qrcodeShow.showImg()
                    x, y = 1, 1
                elif '登录成功' in qrStatus:
                    # print(qrStatus)
                    log.info('已获授权')
                    items = qrStatus.split(',')
                    self.nick = str(items[-1].split("'")[1])
                    self.qq = str(int(self.session.cookies['superuin'][1:]))
                    self.urlPtwebqq = items[2].strip().strip("'")
                    print("urlPtwebqq:",self.urlPtwebqq)
                    t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
                    self.dbbasename = '%s-%s-contact.db'%(t, self.qq)
                    self.dbname = self.dbbasename
                    print("self.dbname :",self.dbname)
                    break
                else:
                    log.error('获取二维码扫描状态时出错, html="%s"', qrStatus)
                    sys.exit(1)
        except Exception as e:
            log.error(e)

    def getPtwebqq(self):
        try:
            print(self.session.cookies)
            self.getUrl(self.urlPtwebqq)
            self.ptwebqq = self.session.cookies['ptwebqq']
            log.info("已获取ptwebqq")
        except Exception as e:
            print(e)

    def getVFwebqq(self):
        try:
            self.getUrl(self.urlPtwebqq)# 获取登录成功的session
            url = "https://s.web2.qq.com/api/getvfwebqq?ptwebqq=%s&clientid=%s&psessionid=&t=%s" \
                  %(self.ptwebqq,self.clientid,repr(random.random()* 900000 + 1000000))
            Referer = "https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1"
            Origin = 'https://s.web2.qq.com'
            vfwebqq = self.smartRequest(url)['vfwebqq']
            self.vfwebqq = vfwebqq
            self.ptwebqq = ''
            # print(self.vfwebqq)
            # self.vfwebqq = self.smartRequest(url)# 获取vfwebqq
            log.info('已经获取vfwebqq')
        except Exception as e:
            print(e)

    # 获取各种登录参数后真正的登录了
    def getUinandPsessionId(self):
        result = self.smartRequest(
            url='https://d1.web2.qq.com/channel/login2',
            data={
                'r': json.dumps({
                    'ptwebqq': self.ptwebqq, 'clientid': self.clientid,
                    'psessionid': '', 'status': 'online'
                })
            },
            Referer="https://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2",
            Origin="https://d1.web2.qq.com"
        )
        if result is not  None:
            self.uin = result['uin']
            self.psessionid = result['psessionid']
            self.hash = qHash(self.uin, '')
            self.bkn = bknHash(self.session.cookies['skey'])
            log.info('已获取uin和psessionid')

    # requests
    def smartRequest(self, url, data=None, Referer=None, Origin=None):
        resp = self.getUrl(url, data, Referer, Origin)
        # print(resp.content)
        if resp.status_code == 200:
            reJs = resp.json()
            if reJs['retcode'] == 0:
                return reJs['result']
            else:
                None

    def poll(self):
        try:
            result = self.smartRequest(
                url = 'https://d1.web2.qq.com/channel/poll2',
                data = {
                    'r':json.dumps({
                        'ptwebqq':self.ptwebqq,'clientid':self.clientid,
                        'pessionid':self.psessionid,'key':''
                    })
                },
                Referer="https://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2",
                Origin="https://d1.web2.qq.com",
                # expectedCodes = (0,100003,100100,100012)
            )
            print(result)
            ctype = {
                'message':'buddy',
                'group_message':'group',
                'discu_message':'discuss'
            }
        except Exception as e:
            print(e)

def bknHash(skey, init_str=5381):
    hash_str = init_str
    for i in skey:
        hash_str += (hash_str << 5) + ord(i)
    hash_str = int(hash_str & 2147483647)
    return hash_str

def qHash(x, K):
    N = [0] * 4
    for T in range(len(K)):
        N[T % 4] ^= ord(K[T])

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
    ba.loginAction(conf="")
    ba.poll()