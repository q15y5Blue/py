#coding:utf8
from demo.Until.pyMySqlDB import connectionClazz

def updateUrls(urlName,urlHref):
    try:
        connect=connectionClazz.connection
        with connect.cursor() as cursor:
            sql ="insert into urls (urlName,urlHref) values(%s,%s)";
            #执行sql语句
            print("目前执行的sql语句是："+sql)
            cursor.execute(sql,(urlName,urlHref))
            print(cursor.execute(sql,(urlName,urlHref)))
    finally:
        connect.close()

print(updateUrls("百度","http://www.baidu.com"))