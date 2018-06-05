# coding:utf-8
import MySQLdb
import json


def get_connect():
    db_connect = MySQLdb.connect("118.25.187.151", "root", "qiuyu8691689", "qiuyu", charset="utf8mb4")
    return db_connect


def update_info(connect, sql):
    cursor = connect.cursor()
    cursor.execute(sql)
    try:
        connect.commit()
    except:
        connect.rollback()
