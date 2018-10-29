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
        'host':'101.132.243.211',
        'client_flags': [ClientFlag.SSL],
    }

    def __init__(self):
        # create a connection pool implicitly -> conn.connct(pool_name="xxx", pool_size="3", **config)
        self.connect = conn.connect(**self.config)
        # self.pool = pool(pool_name="myPool", pool_size=6, **self.config)

    def __del__(self):
        self.connect.close()

    def get_date(self, sql):
        cursor = self.connect.cursor(buffered=True)
        cursor.execute(sql)
        data = cursor.fetchone()
        cursor.close()
        return data

    def get_allData(self,sql):
        cursor = self.connect.cursor(buffered=True)
        cursor.execute(sql)
        datas = cursor.fetchall()
        cursor.close()
        return datas

    def update_info(self,sql):
        cursor = self.connect.cursor(buffered=True)
        cursor.execute(sql)
        try:
            self.connect.commit()
        except:
            self.connect.rollback()


# if __name__=='__main__':
#     con = DBConnect()
#     print(con.get_date('select location,port from proxy order by rand()'))