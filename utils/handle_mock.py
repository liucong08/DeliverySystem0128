# -*- coding: utf-8 -*-
# @File    : handle_mock.py
# @Time    : 2022/11/9 20:38
# @Author  : xintian
# @Email   : 1730588479@qq.com
# @Software: PyCharm
# Date:2022/11/9
import requests
import time
import threading
HOST = 'http://127.0.0.1:9999'
# def test():
#     url = f'{HOST}/sq'
#     payload = {"key1": "abc", "key2": "123"}
#     resp = requests.get(url, params=payload)
#     print(resp.text)


# ------------申诉接口------------------
def commit_order(data):
    url = f'{HOST}/api/order/create/'
    payload = data
    resp = requests.post(url, json=payload)
    return resp.json()


# --------------查询接口----------------
"""
接口的特性：不是你想查就里面可以查到的，也不能一直循环查
注意事项：
    - 使用具体 id 查询
    - 查询需要频率 单位是s  interval
    - 超时机制：timeout   s
"""


def get_order_result(id, interval=5, timeout=30):
    """
    :param id: 需要查询的id
    :param interval: 频率 但是s
    :param timeout: 超时 30s
    :return: 查询结果
    """
    url = f'{HOST}/api/order/get_result01/'
    payload = {"order_id": id}
    start_time = time.time()
    end_time = start_time + timeout
    cnt = 1  # 查询次数初始值
    while time.time() < end_time:  # 没有超时就可以循环
        resp = requests.get(url, params=payload)
        if resp.text:
            print(f'第{cnt}次查询结果是--->', resp.text)
            return
        else:
            print(f'---第{cnt}次查询没有返回结果，请稍等5s之后再查询---')
        time.sleep(interval)  # 频率
        cnt += 1

    print('---查询超时，请练习平台管理员人工处理---')

if __name__ == '__main__':
    start_time = time.time()  #主线程执行开始时间
    order_data = {
        "user_id": "sq123456",
        "goods_id": "20200815",
        "num": 1,
        "amount": 200.6
    }
    res = commit_order(order_data)
    id = res['order_id']
    print('申诉请求是响应--->', res)
    # 2.查询结果
    #get_order_result(id)
    #-------创建子线程-------------
    # target=  你需要把哪一个函数做成子线程的函数名
    # args  子线程函数的需要传递的参数----要求是元组
    t1 = threading.Thread(target=get_order_result, args=(id,))
    # 设置守护线程: 如果主线程结束了，或者异常退出，子线程也结束！
    t1.setDaemon(True)
    t1.start()

    #------模拟主线程自动化其他接口的执行-  40s------
    for one in range(40):
        print(f'{one}---主线程执行自动化测试')
        time.sleep(1)




    end_time = time.time()  # 主线程执行结束时间
    print(f'主线程执行耗时:{end_time-start_time}s')




"""
编程阶段：
   1- 逻辑功能先实现
   2- 优化：代码结构+执行效率 
沟通：
    领导：这个接口是实现了，但是有没有优化的空间，执行的效率比较低！
分析：
    1- 领导讲的是一个现象，我得沟通分析找到具体的点
    2- 深入分析： time.sleep(5)*6=30s  中间啥都不干
    3- 技术分析：是否可以让中间查询的等待的30s利用
        - cpu分析
            - cpu 密集型
                算法方面：
            - cpu io阻塞
                - sleep
                - requests请求
方案：解决效率问题
    - 1. 多线程: 在一个进程里去创建多个线程去执行多个任务！，进程里的线程共享进程的资源
        - 强调是充利用一个cpu核的资源
    - 2. 多进程:实现多个客户端去执行，并行
        - 强调是充利用多个cpu核的资源
    - 3. 协程 更小的线程
    - 4. 多进程+协程
    扩展方案：
        - pytest自带的分布式模式
            - pytest-xdist     多进程方案
            - pytest-paraller  多线程方案
    


具体实现：多线程实现
    1. 主线程
        是不是整个代码运行自动化测试
    2. 子线程
        查询结果的接口



"""