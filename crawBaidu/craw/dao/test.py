# coding:utf-8
from crawBaidu.craw.dao.db import DBConnect  # ,DBPool
from crawBaidu.craw.dao.entity import users
from crawBaidu.craw.dao.constant import *
import queue as q
import re

def updateReplyInfo():
    con = DBConnect()
    authorListSql = "select user.username,user.id from users user "
    authors = con.get_allData(authorListSql)
    print(len(authors))
    con.closeCnt()
    numb = 0
    for li in authors:
        try:
            if li is not None or li is not "":
                numb = numb + 1
                print("update : ", numb)
                co = DBConnect(pool=po)
                updateReplySql = "UPDATE reply SET author_id = '%s' where author = '%s' " % (li[1], li[0])
                co.update_info(updateReplySql)
                co.closeCnt()
        except Exception as e:
            continue
            error("error", e)

# if __name__=='__main__':
#     user1 = users(username='name',id=5)
#     user2 = users(username='name',id=5)
#     nameList = NameList(100)
#     nameList.addList(user1)
#     print(nameList.existsObj(user2))