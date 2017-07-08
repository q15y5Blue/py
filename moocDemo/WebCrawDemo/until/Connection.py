'''
Created on 2017年7月8日

@author: q15y5Blue
'''
import pymysql
class connectionClazz:
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='qiuyu',
                                port=3306,
                                db='qiuyu',
                                charset='utf8mb4')
    
    
    def getConnection(self):
        connects=pymysql.connect(host='www.qiuyus.win',
                                 user='root',
                                 password='qiuyu8691689',
                                 port=3306,
                                 db='qiuyu',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor
                                 )
        return connects