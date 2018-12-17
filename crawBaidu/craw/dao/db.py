# coding:utf-8
# 弃用,使用Mysql官方库
from crawBaidu.craw.util.log import *
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector.constants import ClientFlag
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector import connect

config = {
    'user': 'qiuyu',
    'database': 'qiuyu',
    'password': 'qiuyu8691689',
    'host': 'db.yqius.site',
    'charset': 'utf8mb4',
    'client_flags': [ClientFlag.SSL],
}

class DBPool(object):
    def __init__(self):
        self.createPool()

    def createPool(self):
        try:
            self.pool = MySQLConnectionPool(pool_name="myPool", pool_size=12, **config)
            info("pool created")
        except:
            error("SomeError")


class DBConnect(object):
    def __init__(self, pool=None):
        if pool is None:
            self.connect = connect(**config)
        elif pool is not None:
            self.connect = pool.get_connection()


    def get_date(self, sql):
        cursor = self.connect.cursor(buffered=True)
        cursor.execute(sql)
        data = cursor.fetchone()
        cursor.close()
        return data

    def closeCnt(self):
        try:
            # info("connection returned")
            self.connect.close()
        except Exception as e:
            error("关闭失败 ", e)

    def get_allData(self, sql):
        cursor = self.connect.cursor(buffered=True)
        cursor.execute(sql)
        datas = cursor.fetchall()
        cursor.close()
        return datas

    def update_info(self, sql):
        cursor = self.connect.cursor(buffered=True)
        try:
            cursor.execute(sql)
            self.connect.commit()
            cursor.close()
        except Exception as e:  #
            notset(e)
            self.connect.rollback()


# if __name__=='__main__':
#     pool = DBPool()
#     db = DBConnect(pool=pool.pool)
#     sql = 'select location,port from proxy order by rand()'
#     print(type(db.connect))
#     print(db.get_date(sql))
#     print(db.get_date(sql))
#     print(db.get_date(sql))