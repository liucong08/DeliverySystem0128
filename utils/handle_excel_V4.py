# -*- coding: utf-8 -*-
# @File    : handle_excel.py
# @Time    : 2023/2/15 20:20
# @Author  : xintian
# @Email   : 1730588479@qq.com
# @Software: PyCharm
# Date:2023/2/15
import xlrd
import json
from utils.handle_yaml import get_yml_data
from utils.handle_path import data_path, config_path
import os

# -----------------------------V4.0----------------------------
"""
需求：优化bug
需求分析：
    1- 获取到的请求体数据需要给 login登录接口的，但是登录的in_data 什么数据---字典，需要加密！
        要点： 是json就转换成字典，不是json比如是 标题，还是保留字符串类型！
    2- 自动化核心的目标：提效！！！
        自动化本身价值点在回归阶段----高效执行回归----定制化执行用例 /模块
解决方案：
    自动化核心的目标：提效！！！
      - 用例筛选场景：
        - 1. 全部运行！ all
        - 2. 部分运行
            - 单个用例运行
            - 连续几个用例运行
            - 间隔几个用例运行    
"""


def get_excel_data(sheet_name, case_name, run_case=None):
    """
    :param file_path:  文件路径
    :param sheet_name: 表名  sheet——name
    :param args: 需要获取的哪些列
    :return:
    """
    res_list = []
    col_index = []  # 列编号值
    run_case_list = []  # 存放实际运行的用例
    # --------------------------获取配置------------
    case_data = get_yml_data(os.path.join(config_path, 'excelDataConfig.yml'))
    file_path = os.path.join(data_path, case_data['file_name'])
    args = case_data['cols']

    # 1.打开指定路径的文件；work_book---excel文件对象  formatting_info=True  保持原样式
    work_book = xlrd.open_workbook(file_path, formatting_info=True)
    # 2.选择你需要操作的sheet表；---work_sheet 表对象
    work_sheet = work_book.sheet_by_name(sheet_name)

    # -----------------处理列名操作--------------------
    """
    示例： *args ==  装包成元组类型：('请求参数','响应预期结果')
    结果：获取对应的列编号
    """
    for one in args:  # ('请求参数','响应预期结果')
        # 获取第0行列表数据
        col_index.append(work_sheet.row_values(0).index(one))
    # print('获取的列编号是--->', col_index)
    # -----------------处理列名操作 end----------------

    # -----------------用例筛选----------------------
    # 示例：run_case = ['all','001','003-005','009']

    if run_case is None or 'all' in run_case:
        # 1. 运行全部！---第0列用例数据
        run_case_list = work_sheet.col_values(0)  # [‘Login001’,‘Login002’]
    else:
        # 2.部分执行----需要获取里面的执行的用例
        for case_num in run_case:  # '001','003-005','009'
            if '-' in case_num:  # 连续的    '003-005'
                start, end = case_num.split('-')  # start ‘003’ end ‘005’
                for num in range(int(start), int(end) + 1):  # for  num in range(3,5+1)
                    run_case_list.append(f'{case_name}{num:0>3}')  # f'{Login}{003}'
            else:  # 单个   '009'
                run_case_list.append(f'{case_name}{case_num:0>3}')
    # print('筛选执行用例列表--->', run_case_list)
    # -----------------用例筛选 end------------------

    row_index = 0  # 行的初始值
    for col_text in work_sheet.col_values(0):  # 遍历第0列的内容
        if case_name in col_text and col_text in run_case_list:
            col_data = []  # 存放当前行的几列数据的列表
            for col_cnt in col_index:  # [9,11]
                tmp = is_json(work_sheet.cell(row_index, col_cnt).value)
                # 把当前行的几列数据保存在列表数据里
                col_data.append(tmp)
            res_list.append(tuple(col_data))

        row_index += 1  # 每获取一个列内容，跳到下一行操作
    return res_list


def is_json(in_str):
    """
    判定是否json，
    :return:
        1. 是json，返回字典
        2. 不是json，返回原字符串
    """
    try:
        return json.loads(in_str)  # 把json转化字典
    except:
        return in_str


if __name__ == '__main__':
    res = get_excel_data('登录模块', 'Login', run_case=['006', '003-005'])
    for one in res:
        print(one)

"""
测试反馈：
    1.很多函数做到很通用/灵活，需要传递的参数就很多，参数数量多
分析;
    - 哪些参数一般是比较固定
        - 文件路径
        - 列数据

"""
