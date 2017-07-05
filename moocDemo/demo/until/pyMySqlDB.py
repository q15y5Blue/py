import pymysql
import pymysql.cursors

#连接数据库的类
#注意这两种方法有什么不同
class connectionClazz:
#获取数据库链接

    #类变量,赋值后总存在不修改。被共享
    connection = pymysql.connect(host='www.qiuyus.win',
                                user='root',
                                password='qiuyu8691689',
                                port=3306,
                                db='qiuyu',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    
        
    #这是一个实例方法，只能被实例对象调用
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