#-*- coding: utf-8 -*-
#@File    : test_login.py
#@Time    : 2022/10/31 21:54
#@Author  : xintian
#@Email   : 1730588479@qq.com
#@Software: PyCharm
#Date:2022/10/31 
import pytest
import allure
import os
from libs.login import Login
from common.apiAssert import ApiAssert
from utils.handle_excel_V2 import get_excel_data
from utils.handle_path import data_path
from utils.handle_yaml import get_yml_data
@allure.epic('订餐系统')
@allure.feature('登录模块')
class TestLogin:
    """ 登录的测试类 """

    @pytest.mark.parametrize('title,body,resp_exp',
                             get_excel_data(os.path.join(data_path,'Delivery_System_V1.5.xls'), '登录模块', 'Login', '标题', '请求参数', '响应预期结果'))
    @allure.story('登录接口')
    @allure.title('{title}')
    def test_login(self, title, body, resp_exp):
        """登录的测试方法"""
        # 1.执行请求发送
        res = Login().login(body)
        # 2.做断言
        #assert res['msg'] == resp_exp['msg']
        ApiAssert.api_assert(res, '==', resp_exp, 'msg',msg='登录接口的断言')

if __name__ == '__main__':
    pytest.main([__file__, '-s', '--alluredir', '../outFiles/report/tmp', '--clean-alluredir'])
    os.system('allure serve ../outFiles/report/tmp')
    """
    pytest框架：执行的作用----生成执行后的结果数据  xxx.json
    allure 需要显示的：只是一个报告的框架---空壳子---需要执行用例的结果数据做装饰
    """