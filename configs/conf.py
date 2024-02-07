#-*- coding: utf-8 -*-
#@File    : conf.py
#@Time    : 2022/10/30 10:48
#@Author  : xintian
#@Email   : 1730588479@qq.com
#@Software: PyCharm
#Date:2022/10/30

HOST = 'http://42.192.62.8:8082/'
NAME_PWD = {'username': 'ct0980', 'password': '92932'}

class MysqlConfig:
    HOST = '192.168.122.136'
    PORT = 3306
    USER = 'root'
    PWD = 'sq'
    DB = "sq-waimai"
    CHARSET = 'utf8'

class MongoConfig:
    HOST = '192.168.122.136'
    PORT = 27017
    USER = 'admin'
    PWD = 'sq'
    DB = "sq-waimai"