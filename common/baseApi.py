# -*- coding: utf-8 -*-
# @File    : baseApi.py
# @Time    : 2022/10/28 21:50
# @Author  : xintian
# @Email   : 1730588479@qq.com
# @Software: PyCharm
# Date:2022/10/28
import requests
"""
1个请求里对于的用例：不变的是：请求方法，url，请求头;变的是哪一个：参数，预期响应
执行用例的自动化测试：使用ddt
    - excel
    - yaml
把url 和 method单独配置yaml
"""
from configs.conf import HOST
from utils.handle_loguru import log
from utils.handle_yaml import get_yml_data
from utils.handle_path import config_path
import os
import traceback
class BaseAPI:
    """接口的基类，所有的业务类都需要继承的"""
    # 每一个业务都会去继承这个基类，都会创建实例，拿到自己的接口数据
    def __init__(self, user_token=None, **kwargs):  # uid=abdcffgg
        self.data = get_yml_data(os.path.join(config_path,'caseConfig.yaml'))[self.__class__.__name__]
        # 不是所有模块都独运传递token，只有后续业务模块才需要关联token
        if user_token:  #业务模块
            self.header = {'Authorization': user_token}
            self.header.update(kwargs)  # 如果一些特定模块有其他的头的参数 比如 uid可以再增加
        else:  # 登录模块
            self.header = None

        #print('模块的请求头--->', self.header)


    # 公共的发送方法:请求方法、url
    def request_send(self, id='', **kwargs):  # ** 定义关键字参数-装包
        try:
            __config_data = self.data[inspect.stack()[1][3]]
            resp = requests.request(
                method=__config_data['method'],
                url=f"{HOST}{__config_data['path']}{id}",
                headers=self.header,
                **kwargs)  # ** 展开关键字参数--解包
            log.info(f"""模块名:{self.__class__.__name__},接口名:{inspect.stack()[1][3]}
    响应状态码:{resp.status_code},
    请求url:{resp.request.url},
    请求方法:{resp.request.method}""")

            return resp.json()
        except Exception as error:
            log.error(traceback.format_exc())
            print('---请求有错误，请检查---')
            return '---请求有错误，请检查---'
            # 日志处理

    # ---------封装增删改查方法-------------
    # 为什么需要封装： 我们在BaseAPI这个父类封装了增删改查方法，后续其他业务模块继承父类
    # 如果子类没有特殊需求，不写具体的增删改查，去继承父类方法
    # 如果子类有特殊需求，重写父类的 增删改查

    # 查询方法
    def query(self, data):
        return self.request_send(params=data)

    # 增加方法: 可以是 josn  也可以是表单
    def add(self, **kwargs):
        return self.request_send(**kwargs)

    # 修改方法
    def update(self, id='',**kwargs):
        return self.request_send(id=id,**kwargs)

    # 删除方法
    def delete(self, id):
        return self.request_send(id=id)

    # 文件上传接口
    """
    Content-Disposition: form-data; name="file"; filename="123.png"
    Content-Type: png/gif

    PNG
    文件上传接口需要传递的参数：给哪一个变量，文件名，文件类型，文件本身的数据
    {‘变量名’:(文件名,文件本身数据,文件类型)}
    {'file':('123.png',open(文件路径，'rb'),'image/png')}
    """
    # ../data/123.png
    def file_upload(self, file_path: str):
        # 文件名
        file_name = file_path.split('/')[-1]  # 123.png
        file_type = file_path.split('.')[-1]  # png
        user_file = {'file': (file_name, open(file_path, 'rb'), file_type)}
        return self.request_send(files=user_file)





import inspect
if __name__ == '__main__':

    # test()函数
    def test():
        # 我需要打印是哪一个函数调用了我，他的函数名是什么？
        print('---执行test函数---')
        # 函数栈信息
        print('调用我的函数名是--->', inspect.stack()[1][3])

    def a():
        test()

    def b():
        test()

    a()
    b()