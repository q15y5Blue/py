import pymysql
import pymysql.cursors

class connectionClazz:
#获取数据库链接
    connection = pymysql.connect(host='www.qiuyus.win',
                                 user='root',
                                 password='qiuyu8691689',
                                 db='qiuyu',
                                 charset='utf8mb4',
                                 )

