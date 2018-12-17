# coding:utf-8
# 弃用,使用Mysql官方库
import MySQLdb
import mysql.connector as conn
from mysql.connector.pooling import MySQLConnectionPool as Pool
from mysql.connector.constants import ClientFlag
from mysql.connector.errors import InterfaceError as inError
config = {
    'user': 'qiuyu',
    'database': 'qiuyu',
    'password': 'qiuyu8691689',
    'host': 'db.yqius.site',
    'charset': 'utf8mb4',
    'client_flags': [ClientFlag.SSL],
}
# pool = Pool(pool_name="myPool", pool_size=8, **config)

class DBPool(object):
    def __init__(self):
        self.pool = Pool(pool_name="myPool", pool_size=12, **config)

class DBConnect(object):
    def __init__(self):
        self.pool = DBPool()
        self.connect = self.getCon()

    def getCon(self):
        try:
            return self.pool.pool.get_connection()
        except Exception as e:
            print("连接出错:", e)

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
            print("关闭失败 ",e)
            pass

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
        except:
            self.connect.rollback()
