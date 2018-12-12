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
        self.connect = conn.connect(**self.config)

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