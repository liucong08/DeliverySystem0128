# -*- coding: utf-8 -*-
# @File    : handle_excel.py
# @Time    : 2022/10/31 20:10
# @Author  : xintian
# @Email   : 1730588479@qq.com
# @Software: PyCharm
# Date:2022/10/31
import xlrd
import json

"""
------------------------V2.0----------------------
优化需求：
    - 1. 如果需要获取其他列数据---得修源代码
    - 2. 数据格式，不符合数据的需求！
解决方案：
    - 1.使用*args参数
        - 直接使用 列编号 1，2，3  特点：可读性差，但是代码处理简单
        - 使用列名  请求参数,标题；特点：可读性好，代码不能直接去传递，需要转换
    - 2 数据格式问题
        - 需要把请求参数json格式---变成登录接口可以加密的字典----json.loads()
        - 注意事项：
            如果是json可以使用-json.loads()
            如果不是，不能去转换
"""


def get_excel_data(file_path, sheet_name, case_name, *args):
    res_list = []
    col_indexs = []  # 存放列编号

    # 1.打开excel文件--在磁盘，代码需要操作，需要加载到内存里
    work_book = xlrd.open_workbook(file_path, formatting_info=True)
    # 2.操作对应的表
    work_sheet = work_book.sheet_by_name(sheet_name)

    # -----------------------下面是重要----------------------
    """
    示例：args = '请求参数','预期响应数据'
    args得到是一个元组
    """
    for one in args:  # '请求参数',    '预期响应数据'-----列编号
        col_indexs.append(work_sheet.row_values(0).index(one))  # 表头是一个列表，使用index 求值所在的下标
    # -----------------------------------------------------

    print('用户需要获取的数据的列编号是--->', col_indexs)
    row_index = 0  # 行编号初始值
    for one in work_sheet.col_values(0):
        if case_name in one:
            col_data = []
            for index in col_indexs:  # 需要获取列的编号-- [9,11，12]
                tmp = is_json(work_sheet.cell(row_index, index).value)  # 列编号有几个，就执行几次循环
                col_data.append(tmp)  # 这一行的 这个几列数据的结果
            res_list.append(tuple(col_data))  #
        row_index += 1  # 行号加

    return res_list


# 封装一个判断是否是json函数
def is_json(str):
    """
     str: 需要判断的字符串数据
    :return: 结果
    """
    try:
        return json.loads(str)  # 是json字符串-----直接返回转换后的字典数据
    except:
        return str  # 不是json--原符串返回


if __name__ == '__main__':
    get_excel_data('../data/Delivery_System_V1.5.xls', '登录模块', 'Login', '标题', '请求参数')

"""
测试反馈：
    - 1. 不能选择某一个，或者某些用例执行
    - 2. 函数需要传递的参数太多了
"""

# --------小扩展---------
# a = [10,20,30]
# name = ['xiaoming','xt','sq']
# res = zip(a,name)
# print(list(res))
