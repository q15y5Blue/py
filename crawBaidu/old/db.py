# coding:utf-8
# 弃用,使用Mysql官方库
# import MySQLdb
import mysql.connector as conn
from mysql.connector.pooling import MySQLConnectionPool as pool
from mysql.connector.constants import ClientFlag

class DBConnect(object):
    config = {
        'user':'qiuyu',
        'database':'qiuyu',
        'password':'qiuyu8691689',
        'host':'db.yqius.site',
        'charset':'utf8mb4',
        'client_flags': [ClientFlag.SSL],
    }

    def __init__(self):
        # create a connection pool implicitly -> conn.connct(pool_name="xxx", pool_size="3", **config)
        self.connect = conn.connect(**self.config)
        # self.pool = pool(pool_name="myPool", pool_size=6, **self.config)

    def __del__(self):
        try:
            self.connect.close()
        except Exception as e:
            print(e)

    def get_date(self, sql):
        cursor = self.connect.cursor(buffered=True)
        cursor.execute(sql)
        data = cursor.fetchone()
        cursor.close()
        return data

    def closeCnt(self):
        try:
            self.connect.close()
        except Exception as e:
            print(e)

    def get_allData(self,sql):
        cursor = self.connect.cursor(buffered=True)
        cursor.execute(sql)
        datas = cursor.fetchall()
        cursor.close()
        return datas

    def update_info(self, sql):
        cursor = self.connect.cursor(buffered=True)
        cursor.execute(sql)
        try:
            self.connect.commit()
        except:
            self.connect.rollback()

#
# if __name__=='__main__':
#     con = DBConnect()
#     str = '😂'
#     sql = "select id,author,content,date,floor_num,fn,article_id from reply where fn !=0"
#    #sql = "insert into reply_lzz('id','author','content','date','floor_num','fn','reply_id') values (select id,author,content,date,floor_num,fn,article_id from reply where fn !=0)" %(str)
#     for li in con.get_allData(sql):
#         con.update_info("insert into reply_lzz(id,author,content,date,floor_num,fn,reply_id) values('%s','%s','%s','%s','%s','%s','%s')"\
#                         %(li[0],li[1],li[2],li[3],li[4],li[5],li[6]))
#     con.connect.close()
