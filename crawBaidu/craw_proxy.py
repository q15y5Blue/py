# coding:utf-8
from crawBaidu.headers import headers
from crawBaidu.conection import *
from crawBaidu.db import DBConnect
from bs4 import BeautifulSoup
import requests
import requests.exceptions as exc
import re
import time


class NetProtocol(object):
    def __init__(self, location=None, port=None):
        self.location = location
        self.port = port
        self.ip = self.__str__()
        self.prox = {'http': self.ip, 'https': self.ip}
        if self.location == None and self.port==None:
            self.getIp()

    def __str__(self):
        if self.location == None or self.port ==None:
            return ""
        else:
            return self.location + ":"+ self.port

    # 初始化ip
    def getIp(self):
        cnt = DBConnect()
        sql = "select location,port from proxy order by rand()"
        data = cnt.get_date(sql)
        self.location = data[0]
        self.port = data[1]
        self.ip = self.__str__()
        self.prox = {'http': self.ip, 'https': self.ip}

    #获取所有proxies
    def getProxies(self):
        cnt = DBConnect()
        sql = "select location,port from proxy "
        data = cnt.get_allData(sql)
        list = []
        for dat in data:
            list.append(dat[0] + ':' + dat[1])
        return list

    #获取某个
    def getTheProxyes(self, cnt):
        sql = "select location from proxy where location = '%s' " %(self.location)
        data = cnt.get_date(sql)
        return data

    # 获取每一个页的ipList http://www.66ip.cn/%s.html
    def craw_ipList(self, url):
        req = requests.get(url, timeout=120)
        req.encoding = "utf-8"
        soup = BeautifulSoup(req.text, "html.parser")
        table_li = soup.find_all("table", width="100%").__getitem__(0)
        exp_ip = re.compile("(?<=<td>)(\d{1,3}.){3}\d{1,3}(?=</td>)")
        exp_port = re.compile("(?<=<td>)\d{1,5}(?=</td>)")
        tr_li = table_li.find_all("tr")
        ipList = []
        for tr in tr_li:
            strs = str(tr)
            location_ip = exp_ip.search(strs)
            location_port = exp_port.search(strs)
            if type(location_ip).__name__ == "SRE_Match" and type(location_port).__name__ == "SRE_Match":
                location = str(location_ip.group(0))
                port = str(location_port.group(0))
                ip = NetProtocol(location=location, port=port)
                ipList.append(ip)
        return ipList

    # 执行爬虫,并将代理存到数据库中
    def pagingCraw(self):
        list = []
        for x in range(1, 35):
            url = "http://www.66ip.cn/%s.html" % (x)
            list.extend(self.craw_ipList(url))
        # importData
        cnt = DBConnect()
        for lis in list:
            if lis.testProxy():
                sql = "insert into proxy(location,port) values ('%s','%s')" % (lis.location, lis.port)
                if not lis.getTheProxyes(cnt):
                    cnt.update_info(sql)
        # return list

    # testProxy
    def testProxy(self):
        url = "http://icanhazip.com/"
        print("正在测试代理连接", self.prox)
        try:
            req = requests.get(url, proxies=self.prox)
            if req.text.strip() == str(self.location).strip():
                return True
        except Exception:
            return False

    def deleteProxy(self):
        db = DBConnect()
        if self.getTheProxyes(db) is not None:
            db.update_info("delete from proxy where location='%s'"%(self.location))



if __name__ == '__main__':
    pro = NetProtocol()
    # if pro.testProxy() == True:
    #     req = requests.get("https://tieba.baidu.com/f?kw=%CB%AB%C3%CE%D5%F2&pn=0&", pro.prox)
    #     print(req.status_code)
    pro.pagingCraw()