#coding:utf8

from demo.until.pyMySqlDB import connectionClazz
from demo.entity.news import News

#更新
def updateNewsObj (news=News()):
    try :
        connect=connectionClazz.connection
        print("打开一个公用连接")
        with connect.cursor() as cursors:
            sql="insert into news(content,url,author,src,tim) values (%s,%s,%s,%s,%s)"
            print("执行了sql语句:",sql)
            #执行
            cursors.execute(sql,(news.content,news.url,news._authors,news.src,news.tim))
            #提交
            connect.commit()
    finally :
        cursors.close()
        print("关闭游标")

#########总觉得这里也是一个BUG#，待解决##################################################################
        #connect.close()

#查询        
def selectAllNews():
    try :
        #connect=connectionClazz.connection
        connect=connectionClazz.getConnection(0)
        with connect.cursor() as cursors:
            sql="select * from news"
            print("执行了sql语句",sql)
            cursors.execute(sql)#得到总记录数
            #cursor.fetchone() //查询下一行
            #cursor.fetchmany(size=None) //得到指定大小
            row =cursors.fetchall()#fetchall 获取全部
            connect.commit()
    finally:
        cursors.close()
        connect.close()
        print("关闭一个连接")
        return row
