#coding:utf8

from demo.until.pyMySqlDB import connectionClazz
from demo.entity.news import News

#更新
def updateNewsObj (news=News()):
    try :
        connect=connectionClazz.connection
        with connect.cursor() as cursors:
            sql="insert into news(content,url,author,src,tim) values (%s,%s,%s,%s,%s)"
            print("执行了sql语句：",sql)
            #执行
            cursors.execute(sql,(news.content,news.url,news._authors,news.src,news.tim))
            #提交
            connect.commit()
    finally :
        connect.close()

#查询        
def selectAllNews():
    try :
        connect=connectionClazz.connection
        with connect.cursor() as cursors:
            sql="select * from news"
            print("执行了sql语句",sql)
            cursors.execute(sql)
            row =cursors.fetchall()
            connect.commit()
    finally:
        connect.close()
        return row

