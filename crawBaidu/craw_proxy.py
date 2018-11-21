# coding:utf-8
from crawBaidu.headers import headers
from crawBaidu.conection import *
from crawBaidu.db import DBConnect
from bs4 import BeautifulSoup
import requests
import requests.exceptions as exc
import re
import time

head = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
}
MyCookies = {
    'Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59':'1542763729',
    'Hm_lvt_0cf76c77469e965d2957f0553e6ecf59':'1542763640',
    '_free_proxy_session':'BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTI3OWE3MGRlNDNjOGUyYWI5M2Q4N2VkMjY0Mzg5NTQzBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUJBcDY3TFpMTGFwQWZxL0UwdFZibS95T2plM25pb0dHWStkM1ZlK2NvMmM9BjsARg',
}
class NetProtocol(object):
    def __init__(self, location=None, port=None, type=None):
        self.location = location
        self.port = port
        self.type = type
        self.ip = self.__str__()#:
        self.prox = {'http': self.ip, 'https': self.ip}
        if self.location is None and self.port is None and type is None:
            self.getIp()

    def __str__(self):
        if self.location == None or self.port ==None:
            return ""
        else:
            return self.location + ":"+ self.port

    # 初始化ip
    def getIp(self):
        cnt = DBConnect()
        try:
            sql = "select location,port from proxy order by rand()"
            data = cnt.get_date(sql)
            self.location = data[0]
            self.port = data[1]
            self.ip = self.__str__()
            self.prox = {'http': self.ip, 'https': self.ip}
        except Exception as e:
            print("代理吃空了，放缓爬虫速度")
            time.sleep(2)
        cnt.closeCnt()

    #获取所有proxies
    def getProxies(self):
        cnt = DBConnect()
        sql = "select location,port from proxy "
        data = cnt.get_allData(sql)
        list = []
        cnt.closeCnt()
        for dat in data:
            list.append(dat[0] + ':' + dat[1])
        return list


    #获取某个
    def getTheProxyes(self, cnt):
        sql = "select location from proxy where location = '%s' " %(self.location)
        data = cnt.get_date(sql)
        return data

    def craw_ipList(self,url):
        req = requests.get(url, timeout=12, headers=head)
        print(req.status_code)
        if req.status_code == 200:
            ipList = []
            req.encoding="utf-8"
            soup = BeautifulSoup(req.text,"html.parser")
            tableList = soup.find("table", id="ip_list")
            trList = tableList.find_all("tr")
            exp_ip = re.compile("(?<=<td>)(\d{1,3}.){3}\d{1,3}(?=</td>)")
            exp_port = re.compile("(?<=<td>)\d{1,5}(?=</td>)")
            exp_type = re.compile("(?<=<td>)HTTP[S](?=</td>)")
            for tr in trList:
                location_ip = exp_ip.search(str(tr))
                location_port = exp_port.search(str(tr))
                location_type = exp_type.search(str(tr))
                if type(location_ip).__name__ == "SRE_Match" and type(location_port).__name__ == "SRE_Match" and type(location_type).__name__=='SRE_Match':
                    location = str(location_ip.group(0))
                    port = str(location_port.group(0))
                    types = str(location_type.group(0))
                    ip = NetProtocol(location=location, port=port,type=types)
                    ipList.append(ip)
            return ipList

    # 执行爬虫,并将代理存到数据库中
    def pagingCraw(self):
        list = []
        flag = 0
        for x in range(1, 35):
            url = "http://www.xicidaili.com/nn/%d"%(x)
            reList= self.craw_ipList(url)
            if reList is not None:
                list.extend(reList)
                flag = 1
        if flag ==1:
            cnt = DBConnect()
            for lis in list:
                if lis.testProxy():
                    sql = "insert into proxy(location,port,type) values ('%s','%s','%s')" % (lis.location, lis.port, lis.type)
                    if not lis.getTheProxyes(cnt):
                        cnt.update_info(sql)
            cnt.closeCnt()

    # testProxy
    def testProxy(self):
        url = "http://icanhazip.com/"
        print("正在测试代理连接",self.prox)
        try:
            req = requests.get(url, proxies=self.prox, headers=head)
            if req.text.strip() == str(self.location).strip():
                print( self.prox,"代理可用")
                return True
        except Exception:
            return False

    def deleteProxy(self):
        db = DBConnect()
        if self.getTheProxyes(db) is not None:
            db.update_info("delete from proxy where location='%s'"%(self.location))
        db.closeCnt()



if __name__ == '__main__':
    pro = NetProtocol()
    pro.pagingCraw()