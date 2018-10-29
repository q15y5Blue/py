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
    def __init__(self):
        self.location = ''
        self.port = ''
        self.ip = ''
        self.getIp()
        self.prox =  {'http': self.ip, 'https': self.ip}

    def __str__(self):
        return self.location + ":"+ self.port

    def getIp(self):
        cnt = DBConnect()
        sql = "select location,port from proxy order by rand()"
        data = cnt.get_date(sql)
        self.location = data[0]
        self.port = data[1]
        self.ip = self.__str__()

    def getProxies(self):
        cnt = DBConnect()
        sql = "select location,port from proxy "
        data = cnt.get_allData(sql)
        list = []
        for dat in data:
            list.append(dat[0] + ':' + dat[1])
        return list

    # 获取每一个页的ipList http://www.66ip.cn/%s.html
    def craw_ipList(self,url):
        baseSession = BaseSession()
        req =  baseSession.reqGet(url)
        # req = requests.get(url)
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
                ip = NetProtocol()
                ip.location = str(location_ip.group(0))
                ip.port = str(location_port.group(0))
                ipList.append(ip)
        return ipList

    # testProxy
    def testProxy(self):
        url = "http://icanhazip.com/"
        print("正在尝试使用代理连接", self.prox)
        bs = BaseSession()
        req  = bs.reqGet(url, proxies=self)
        if req:
            print("当前代理可用,代理IP是:",req.text)

    # 执行爬虫,并将代理存到数据库中
    def pagingCraw(self):
        list = []
        for x in range(1, 21):
            url = "http://www.66ip.cn/%s.html" % (x)
            list.extend(self.craw_ipList(url))
            import_date(list)
        # return list

    def deleteProxy(self):
        db = DBConnect()
        db.update_info("delete from proxy where location='%s'"%(self.location))


# 导入数据到proxy表里
def import_date(list):
    cnt = DBConnect()
    for lis in list:
        sql = "insert into proxy(location,port) values ('%s','%s')" % (lis.location, lis.port)
        cnt.update_info(sql)



if __name__ == '__main__':
    proxy = NetProtocol()
    print(proxy.prox)
    proxy.testProxy()
    # pro =netProtocol()
    # datas = pro.getProxies()
    # testProxy(url,datas)