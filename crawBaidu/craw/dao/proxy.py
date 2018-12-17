# coding:utf-8
from crawBaidu.craw.dao.db import DBConnect
from crawBaidu.craw.download.constants import get_headers
import time
import random
import requests

class Proxies(object):
    def __init__(self, db=None): # 代理可用
        if db == None:
            self.location = ''
            self.port = ''
            self.type = ''
            self.ip = self.location + ":"+ self.port
            self.prox = {'http': self.ip, 'https': self.ip}
        else:
            self.getIp()

    def getIp(self):
        cnt = DBConnect()
        try:
            sql = "select location,port from proxy order by rand()"
            data = cnt.get_date(sql)
            self.location = data[0]
            self.port = data[1]
            self.ip = self.location + ":"+ self.port
            self.prox = {'http': self.ip, 'https': self.ip}
        except Exception as e:
            print("代理吃空了，放缓爬虫速度")
            time.sleep(random.uniform(0, 1))
        cnt.closeCnt()

    def __str__(self):
        return str(self.prox)

    # test Proxy
    def testProxy(self):
        url = "http://icanhazip.com/"
        print("正在测试代理连接", self.prox)
        try:
            req = requests.get(url, proxies=self.prox, headers=get_headers)
            if req.text.strip() == str(self.location).strip():
                print(self.prox, "代理可用")
                return True
        except Exception as exc:
            print("测试代理过程中出错",exc)
            return False

    def deleteProxy(self):
        db = DBConnect()
        try:
            db.update_info("delete from proxy where location='%s' " % (self.location))
        except Exception:
            print("删除过程中异常")
        db.closeCnt()

if __name__ == "__main__":
    print(Proxies(db='xx'))