#-*- coding: utf-8 -*-
#@File    : test.py
#@Time    : 2022/11/3 21:39
#@Author  : xintian
#@Email   : 1730588479@qq.com
#@Software: PyCharm
#Date:2022/11/3 
#  增删改查
import requests
def request_send(method):
    if method == 'POST':
        requests.post()
    elif method == 'GET':
        requests.get()
    elif method == 'PUT':
        requests.put()
    elif method == 'DELETE':
        requests.delete()

def request_send(method):
    requests.request(method)
