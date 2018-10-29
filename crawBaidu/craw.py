# coding:utf8
# 以前写的,暂时不用.
import time
from crawBaidu import db as din
import requests
from bs4 import BeautifulSoup

# 头部信息
headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 ' +
                   '(KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
}

class result:
    def __init__(self):
        self.name = "123"
        self.content = "123"
        self.tall = "123"
        self.time = "123"
        self.page = "123"

def get_content(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        # print("响应代码", res.status_code)
        return res.text

# 获取参数
def parseData(html_datas, p):
    soup = BeautifulSoup(html_datas, "html.parser")
    contentList = soup.select(".l_post")  # j_d_post_content
    rs_list = []
    for li in contentList:  # 118.25.187.151
        resul = result()
        name = li.select(".d_name").__getitem__(0).text
        print(name)
        content = li.select(".j_d_post_content")
        tail_info = li.select(".tail-info")
        if(content.__len__()==0):
            continue
        resul.name = name.strip()
        resul.content = content.__getitem__(0).text.strip('').strip()
        resul.page = p
        if(tail_info.__len__() == 3):  #  用电脑时候
            resul.tall = tail_info.__getitem__(1).text
            resul.time = tail_info.__getitem__(2).text
        elif (tail_info.__len__() == 4):  #  手机
            resul.tall = tail_info.__getitem__(2).text
            resul.time = tail_info.__getitem__(3).text
        rs_list.append(resul)
    return rs_list


# 待解决
# _mysql_exceptions.OperationalError: (1366, "Incorrect string value: '\\xF0\\x9F\\x90\\xA785...' for column 'content' at row 1")
def import_date(list):
    connect = din.get_connect()
    # cursor = connect.cursor()
    for lis in list:
        for li in lis:
            # print(li.name,li.content,li.tall,li.time,li.page)
            sql = "insert into infos(name,content,tall,time,page) values ('%s','%s','%s','%s','%s')" % (li.name,li.content,li.tall,li.time,li.page)
            din.update_info(connect, sql)
    connect.close()


if __name__ == "__main__":
    list = []
    for p in range(111, 112):
        time.sleep(0.5)
        print(p)
        url = "https://tieba.baidu.com/p/5726419216?pn=%s" %( p )
        html_datas = get_content(url)
        # print(html_datas)
        # time.sleep(10)
        if html_datas is not None:
            lis = parseData(html_datas, p)
            list.append(lis)
            # print(list)
    import_date(list)
