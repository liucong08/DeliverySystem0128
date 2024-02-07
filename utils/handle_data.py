#-*- coding: utf-8 -*-
#@File    : handle_data.py
#@Time    : 2022/11/11 22:16
#@Author  : xintian
#@Email   : 1730588479@qq.com
#@Software: PyCharm
#Date:2022/11/11 
# 很多时候需要测试人员造数据
# pip install  faker
from faker import Faker

fake = Faker(locale='zh_CN')
print(fake.address())
print(fake.name())