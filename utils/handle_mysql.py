import pymysql
from configs.conf import MysqlConfig

#类封装
class MysqlConnection:
    def __init__(self,host=MysqlConfig.HOST,port=MysqlConfig.PORT,user=MysqlConfig.USER,
                 pwd=MysqlConfig.PWD,db=MysqlConfig.DB):
        #1创建连接
        self.db = pymysql.connect(host=host,port=port,user=user,password=pwd,database=db,
                                  charset=MysqlConfig.CHARSET)
        #2创建游标
        self.cursor = self.db.cursor()

    #查询
    def select(self,sql,many=True):
        """
        查询方法
        :param sql:查询sql语句
        :param many: 控制获取多个结果
        :return: 查询的结果
        """
        try:
            self.cursor.execute(sql)
            if many:
                result = self.cursor.fetchall()
            else:
                result = self.cursor.fetchone()
            return result
        except Exception as e:
            #打日志
            raise e

    #增删改流程都一样 ，可以封装通用方法
    def __do(self,sql):
        try:
            self.cursor.execute(sql)

        except Exception as e:
            #回滚
            self.db.rollback()
            #打日志
            raise e
        else:
            self.db.commit()

    #修改
    def update(self,sql):
        self.__do(sql)
    #插入
    def insert(self,sql):
        self.__do(sql)

    #删除
    def delete(self,sql):
        self.__do(sql)

    #退出方法
    # def exit(self):
    #     self.cursor.close()
    #     self.db.close()
    def __del__(self):
        self.cursor.close()
        self.db.close()


class A:
    def __del__(self): #默认 实例消失以后 默认执行的方法
        print("结束了")
    def hello(self):
        print("hello")
    def hello1(self):
        print("hello1")




if __name__ == '__main__':
    db = MysqlConnection()
    db.update("update t_sys_login_log set ip='localhost' where id=3;")
    # db.exit()
    # a = A()
    # a.hello()
    # a.hello1()