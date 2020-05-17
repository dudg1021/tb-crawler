# -*- coding: utf-8 -*-
import pymysql


# mysql帮助类
class MysqlHelper(object):
    def __init__(self, host, port, db, user, password, charset='utf8'):
        """
        初始化对象
        :param host: 主机地址
        :param port: 端口号
        :param db: 数据库名称
        :param user: 用户名
        :param password: 密码
        :param charset: 字符集
        """
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.charset = charset

    def connect(self, is_dic=False):
        """
        获取数据库连接
        获取游标
        :return:
        """
        self.conn = pymysql.connect(host=self.host, port=self.port, db=self.db, user=self.user, password=self.password,
                                    charset=self.charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor if is_dic is True else pymysql.cursors.Cursor)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e.message)
        return result

    def get_all(self, sql, params=()):
        """
         查询数据集合
        :param sql: 查询的SQL语句
        :param params: 查询参数
        :return: 返回元祖
        """
        list = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            list = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e.message)
        return list

    def get_all_dic(self, sql, params=()):
        """
        返回数据字典集合
        :param sql: 查询的SQL语句
        :param params: 查询参数
        :return: 数据字典集合
        """
        arr = []
        try:
            self.connect(True)
            print(sql)
            self.cursor.execute(sql, params)
            arr = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return arr

    def insert(self, sql, params=()):
        return self.__edit(sql, params)

    def insert_many(self, sql, params=()):
        return self.__edit_many(sql, params)

    def update(self, sql, params=()):
        return self.__edit(sql, params)

    def delete(self, sql, params=()):
        return self.__edit(sql, params)

    def __edit(self, sql, params):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e.message)
        return count

    def __edit_many(self, sql, params):
        count = 0
        try:
            self.connect()
            count = self.cursor.executemany(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count
