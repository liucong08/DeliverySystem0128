#-*- coding: utf-8 -*-
#@File    : handle_decorator.py
#@Time    : 2022/11/11 21:23
#@Author  : xintian
#@Email   : 1730588479@qq.com
#@Software: PyCharm
#Date:2022/11/11 
# 项目的自动化测试脚本已经写好
import time
# def test():
#     print('---自动化开始执行---')
#     time.sleep(1)
#     print('---自动化结束执行---')

# 需求： 是否可以计算出自动化脚本运行的时间

# ---------------方案1---------------------
# def test():
#     start_time = time.time()
#     print('---自动化开始执行---')
#     time.sleep(1)
#     print('---自动化结束执行---')
#     end_time = time.time()
#     print(f'自动化测试执行耗时:{end_time-start_time}s')

"""
方案评估：不可行
    - 如果有100个测试方法，你得修改100次
    - 如果还需要增加功能，你是不是还需要改代码
"""
# ---------------方案2---------------------
"""
需求分析：
    - 1.不能改test源代码
    - 2.这个计时新增功能单独写
"""
# def test():
#     print('---自动化开始执行---')
#     time.sleep(1)
#     print('---自动化结束执行---')
#
# def show_time(func):
#     start_time = time.time()
#     func()
#     end_time = time.time()
#     print(f'自动化测试执行耗时:{end_time-start_time}s')
"""
方案评估：可行,但是有缺陷
    - 这个方案改变了函数的执行方式
    - 
"""
# ---------------方案2---------------------
"""
需求分析：
    - 1.不能改test源代码
    - 2.这个计时新增功能单独写
    - 3.不能改变原有的执行方式
思考：
    - 找经验丰富的同事请教
    - 网上找资料
        - 有一个装饰器的技术可以实现
            - 什么是装饰器
            - 什么使用装饰器
技术扩展：
    装饰器的描述：
        1- 可以理解为高阶的函数
        2- 可以在不改变源代码，为函数增加新功能
        3- 要理解闭包的概念
            - 函数里面定义一个内部函数，内部函数使用了外包函数的变量,外部函数的返回值是内函数的函数对象
"""
# def a(a1):  #外部函数
#     def b():  #内部函数
#         a1 + 1
#     return b



#
# def test():
#     print('---自动化开始执行---')
#     time.sleep(1)
#     print('---自动化结束执行---')
#
#
# def show_time(func):
#     def inner():
#         start_time = time.time()
#         func()
#         end_time = time.time()
#         print(f'自动化测试执行耗时:{end_time-start_time}s')
#     return inner


"""
方案评估：可行,但是有缺陷
    - 每一个测试方法需要增加计时操作都需要增加一行代码
方案解决：
    - 语法糖  @
"""
# ---------------------方案4---使用语法糖--------------------




def show_time(func):
    def inner(*args,**kwargs):
        start_time = time.time()
        res = func(*args,**kwargs) # 其实就是login接口函数
        end_time = time.time()
        print(f'自动化测试执行耗时:{end_time - start_time}s')
        print('心田---新增其他功能代码')
        return res
    return inner

@show_time  # 等价于  test = show_time(test)
def test():
    print('---自动化开始执行---')
    time.sleep(1)
    print('---自动化结束执行---')







if __name__ == '__main__':
    test()   #原代码逻辑调用方式





    # test = show_time(test)  # inner函数对象本身  赋值操作----test变量名=inner函数对象---test==inner
    # test()  # test() ==  inner()


