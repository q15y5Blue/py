# coding:utf8
import time
import json

import requests
from bs4 import BeautifulSoup

# 头部信息
headers = {
     'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
}

class result:
    def __init__(self):
        self.name = ""
        self.content = ""
        self.tall = ""
        self.time = ""

def get_content(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        print(res.status_code)
        return res.text

# 获取参数
def parseData(html_datas):
    soup = BeautifulSoup(html_datas, "html.parser")
    contentList = soup.select(".l_post") #j_d_post_content
    lineNumb = 0
    # print(contentList)
    rs_list = []
    for li in contentList:
        resul = result()
        name = li.select(".d_name").__getitem__(0).text
        content = li.select(".j_d_post_content")
        tail_info = li.select(".tail-info")
        if(content.__len__()==0):
            continue
        resul.name = name
        resul.content = content.__getitem__(0).text.strip('')
        if(tail_info.__len__() == 3):# 用电脑时候
            resul.tall = tail_info.__getitem__(1).text
            resul.time = tail_info.__getitem__(2).text
        elif (tail_info.__len__() == 4):# 手机
            resul.tall = tail_info.__getitem__(2).text
            resul.time = tail_info.__getitem__(3).text
        rs_list.append(resul)
    return rs_list

def import_date(list):
    jsonObj = json.dumps(list)
    file = open("./file.json", "w+")
    file.write(jsonObj)
    file.close()

if __name__ == "__main__":
    pn = 0
    list = []
    for p in range(1, 10):
        print(p)
        url = "https://tieba.baidu.com/p/5692349178?pn=%s" %( p )
        html_datas = get_content(url)
        if html_datas is not None:
            # time.sleep(101)
            list.__add__(parseData(html_datas))
    # html_datas = get_content("https://tieba.baidu.com/p/5692349178")
    import_date(list)
