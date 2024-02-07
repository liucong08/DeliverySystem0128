# -*- coding: utf-8 -*-
# @File    : handle_path.py
# @Time    : 2022/11/7 20:28
# @Author  : xintian
# @Email   : 1730588479@qq.com
# @Software: PyCharm
# Date:2022/11/7
# 处理路径的库 os或者pathlib
import os

# 先获取项目根目录的路径
# print(__file__)
# 上一层路径  ../
# print(os.path.dirname(__file__))
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print('工程根路径--->', project_path)
# data数据路径
data_path = os.path.join(project_path, 'data')
# data数据路径
report_path = os.path.join(project_path, r'outFiles\report\tmp')
# data数据路径
config_path = os.path.join(project_path, 'configs')
# data数据路径
log_path = os.path.join(project_path, r'outFiles\logs')
public_path = os.path.join(project_path, 'utils')
test_path = os.path.join(project_path, 'testCase')