# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 21:26:18 2020

@author: ysl
"""


import pymysql

# 连接数据库

class Database():
    '''
    对mysql的一些操作封装
    '''

    def __init__(self):
        self.db = pymysql.connect('localhost',
                     user = 'root',
                     password = '11703990331',
                     db = 'test' ,
                     port = 3306)
        self.cursor = self.db.cursor()


    def create_table(self):
        '''
        创建表 user
        注意 一旦执行这个，会删除之前的数据，请慎重！
        :return:
        '''
        # 如果数据表已经存在使用 execute() 方法删除表。
        self.cursor.execute("DROP TABLE IF EXISTS user ")
        # 创建数据表SQL语句
        sql = """CREATE TABLE user (
                 id  CHAR(20) NOT NULL,
                 name  CHAR(20) NOT NULL,
                 sex CHAR(6),  
                 telephone CHAR(11) NOT NULL,
                 address CHAR(64),
                 department CHAR(16))"""
        self.cursor.execute(sql)

    def insert(self, id, name, sex, telephone, address, department):
        '''
        插入一人脸信息
        :return:
        '''

        if len(self.search(id)) > 0:
            print('已经存在{}'.format(id))
            return

        sql = '''INSERT INTO user(id,
                 name, sex, telephone, address, department)
                 VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
                '''.format(id, name, sex, telephone, address, department)
        print(sql)
        try:
            #执行sql语句
            self.cursor.execute(sql)
            self.db.commit()
            print('Sucessful')
        except:
            print('failed')
            self.db.rollback()
    def get_table_value(self):
        '''
        获取表内的全部数据
        :return:
        '''
        sql = 'SELECT * FROM user '
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            return results
        except:
            print('Error: unable to fetch data')

    def search(self, id):
        '''
        根据用户id查询是否在表中
        :return:
        '''
        sql = '''SELECT * FROM user \
                 WHERE id = '{}'
               '''.format(id)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()

            return results
        except:
            print('Error: unable to fetch data')
    def close(self):
        self.db.close()


class Record():
    '''
    对mysql的一些操作封装
    '''

    def __init__(self):
        self.db = pymysql.connect('localhost',
                     user = 'root',
                     password = '11703990331',
                     db = 'test',
                     port = 3306)
        self.cursor = self.db.cursor()

    def create_table(self):
        '''
        创建表 record
        注意 一旦执行这个，会删除之前的数据，请慎重！
        :return:
        '''
        # 如果数据表已经存在使用 execute() 方法删除表。
        self.cursor.execute("DROP TABLE IF EXISTS record ")
        # 创建数据表SQL语句
        sql = """CREATE TABLE record (
                 id  CHAR(20) NOT NULL,
                 name  CHAR(20) NOT NULL,
                 date CHAR(32) NOT NULL)
                 """
        self.cursor.execute(sql)

    def insert(self, id, name, date):
        '''
        插入一人脸信息
        :return:
        '''

        sql = '''INSERT INTO record(id,
                 name, date)
                 VALUES ('{}', '{}', '{}')
                '''.format(id, name, date)
        print(sql)
        try:
            #执行sql语句
            self.cursor.execute(sql)
            self.db.commit()
            print('Sucessful')
        except:
            print('failed')
            self.db.rollback()
    def get_table_value(self):
        '''
        获取表内的全部数据
        :return:
        '''
        sql = 'SELECT * FROM record '
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            return results
        except:
            print('Error: unable to fetch data')

    def search(self, id):
        '''
        根据用户id查询是否在表中
        :return:
        '''
        sql = '''SELECT * FROM record \
                 WHERE id = '{}'
               '''.format(id)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            return results
        except:
            print('Error: unable to fetch data')
    def close(self):
        self.db.close()
# # #
# db = Database()
# db.create_table()
# db.close()

# print(db.search('F0000'))
# db.insert('F2008', 'ysl', '20090908')
# db.insert('F2008', '', '', '', '', '')
# db.search('F2009')
# db.close()
# cursor = db.cursor()
# cursor.execute('DROP TABLE IF EXISTS EMPLOYEE')
#
# sql = '''CREATE TABLE user(
#             id CHAR(20) NOT NULL,
#             name CHAR(20) NOT NULL,
#             sex  CHAR(6),
#             telephone CHAR(11) NOT NULL,
#             address CHAR(64)
#             )'''

#sql = """CREATE TABLE EMPLOYEE (
#         FIRST_NAME  CHAR(20) NOT NULL,
#         LAST_NAME  CHAR(20),
#         AGE INT,  
#         SEX CHAR(1),
#         INCOME FLOAT )"""

