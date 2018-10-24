# coding:utf-8
from crawBaidu.headers import headers
import crawBaidu.db as din
from bs4 import BeautifulSoup
import requests
import re


class netProtocol():
    def __init__(self):
        self.location = ""
        self.port = ""
    def __str__(self):
        return self.location + ":"+ self.port

# 获取每一个页的ipList
def craw_ipList(url):
    req = requests.get(url, headers=headers)
    req.encoding = "gb2312"
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
        if type(location_ip).__name__ == "SRE_Match" and type(location_port).__name__=="SRE_Match":
            ip = netProtocol()
            ip.location=str(location_ip.group(0))
            ip.port=str(location_port.group(0))
            ipList.append(ip)
    return ipList

def import_date(list):
    connect = din.get_connect()
    for lis in list:
        sql = "insert into proxy(location,port) values ('%s','%s')" % (lis.location,lis.port)
        din.update_info(connect, sql)
    connect.close()

def pagingCraw():
    list = []
    for x in range(1, 11):
        url = "http://www.66ip.cn/%s.html" % (x)
        list.extend(craw_ipList(url))
    import_date(list)
    # return list


if __name__ == '__main__':
    pagingCraw()
