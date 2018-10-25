# coding:utf-8
import MySQLdb
import json


def get_connect():
    db_connect = MySQLdb.connect("101.132.243.211", "qiuyu", "qiuyu8691689", "qiuyu", charset="utf8mb4")
    return db_connect


def update_info(connect, sql):
    cursor = connect.cursor()
    cursor.execute(sql)
    try:
        connect.commit()
    except:
        connect.rollback()

def get_date(connect, sql):
    cursor = connect.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    return data

def get_allData(connect, sql):
    cursor = connect.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data