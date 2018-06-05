# coding:utf-8
from crawBaidu.headers import headers

from bs4 import BeautifulSoup
import requests
import re

url = "http://www.66ip.cn/1.html"

class obj_ip():
    def __init__(self):
        self.ip_location = ""
        self.port = ""


def craw_ips():
    req = requests.get(url, headers=headers)
    req.encoding = "gb2312"
    soup = BeautifulSoup(req.text, "html.parser")
    table_li = soup.find_all("table", width="100%").__getitem__(0)
    exp_ip = re.compile("(\d{1,3}.){3}\d{1,3}")
    exp_port = re.compile("(^\s)*(\d+)\n")
    tr_li = table_li.find_all("tr")
    for tr in tr_li:
        print(tr.prettify())
        temp_str = tr.prettify()
        location_ip = exp_ip.search(temp_str).__getitem__(0)
        location_port = exp_port.findall(temp_str).__getitem__(1)
        print(location_port)
        if location_ip is not None and location_port is not None:
            obj_ip.ip_location =location_ip
            obj_ip.port =location_port
            # print(exp_ip.search(tr.prettify()))

            #@print(tr.prettify())
            # print(exp_ip.search(tr.string))


if __name__ == '__main__':
    craw_ips()
