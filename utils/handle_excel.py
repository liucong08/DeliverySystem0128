# -*- coding: utf-8 -*-
# @File    : handle_excel.py
# @Time    : 2022/10/31 20:10
# @Author  : xintian
# @Email   : 1730588479@qq.com
# @Software: PyCharm
# Date:2022/10/31
import xlrd
import json
from utils.handle_yaml import get_yml_data
from utils.handle_path import data_path,config_path
import os

"""
需求：需要你写一个读取excel文件代码
需求分析：沟通
    - 1.需要获取什么数据
        - 请求数据
        - 预期的响应
    - 2.需要返回什么样数据类型
        使用场景：这个数据给自动化测试框架使用 pytest做ddt
             [(请求体1,预期响应数据1),(请求体2,预期响应数据2)]
代码方案：
    - 1.打开这个excel文件
    - 2.读取响应列数据
    - 3.组装结果数据
"""


def get_excel_data(file_path, sheet_name, case_name):
    """
    :param file_path: 文件路径
    :param sheet_name:
    :param case_name:
    :return: [(),()]
    """
    res_list = []
    # 1.打开excel文件--在磁盘，代码需要操作，需要加载到内存里
    # formatting_info=True  样式
    work_book = xlrd.open_workbook(file_path, formatting_info=True)
    # 获取所有表的名
    # print(work_book.sheet_names())
    # 2.操作对应的表
    work_sheet = work_book.sheet_by_name(sheet_name)
    # ------------------补充操作-----------------
    # print(work_sheet.row_values(0))  # 获取对应的数据---1行
    # print(work_sheet.col_values(0))  # 获取对应的数据---1列
    # print(work_sheet.cell(0,0).value)  # 获取对应的数据---单元格--cell(行编号,列编号)
    # -----------------------------------------
    row_index = 0  # 行编号初始值
    for one in work_sheet.col_values(0):
        if case_name in one:
            req_body = work_sheet.cell(row_index, 9).value  # 请求数据
            resp_exp = work_sheet.cell(row_index, 11).value  # 预期响应数据
            res_list.append((req_body, resp_exp))  #
        row_index += 1  # 行号加

    for one in res_list:
        print(one)


if __name__ == '__main__':

    get_excel_data(f'{data_path}/Delivery_System_V1.5.xls', '登录模块', 'Login')


"""
-----------------------------v1.0------------------
测试反馈：
    - 1. 如果需要获取其他列数据---得修源代码
    - 2. 数据格式，不符合数据的需求！
"""

# --------小扩展---------
# a = [10,20,30]
# name = ['xiaoming','xt','sq']
# res = zip(a,name)
# print(list(res))
