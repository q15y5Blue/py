#coding:utf8
from demo.until.pyMySqlDB import connectionClazz

#urlName:url名称
#urlHref:路径
def updateUrls(urlName,urlHref):
    try:
        connect=connectionClazz.connection
        with connect.cursor() as cursors:
            sql ="insert into urls (urlName,urlHref) values(%s,%s)";
            #执行sql语句
            print("目前执行的sql语句是：",sql)
            cursors.execute(sql,(urlName,urlHref))#执行
            connect.commit()#提交
    finally:
        connect.close()
