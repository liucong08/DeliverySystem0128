#-*- coding: utf-8 -*-
#@File    : test_shop.py
#@Time    : 2022/11/4 21:29
#@Author  : xintian
#@Email   : 1730588479@qq.com
#@Software: PyCharm
#Date:2022/11/4
import pytest
import allure
import os
from utils.handle_excel_V3 import get_excel_data
from utils.handle_path import data_path, report_path
from common.apiAssert import ApiAssert
"""
fixture函数的调用：
    - 1.没有返回值的fixture函数，直接方法或者类前面使用  @pytest.mark.usefixtures('fixture函数名')
    - 2.有返回值的fixture函数：直接使用fixture函数名就行
        - 执行fixture函数里的代码
        - 拿到它的返回值
"""
@allure.epic('订餐系统')
@allure.feature('店铺模块')
@pytest.mark.shop
class TestShop:
    """ 店铺的测试类 """
    @pytest.mark.parametrize('title,body,exp_data',get_excel_data('我的商铺', 'listshopping'))
    @allure.story('店铺的查询')
    @allure.title('{title}')
    @pytest.mark.shop_query
    def test_shop_query(self, title, body, exp_data, shop_init):
        shop = shop_init  #获取这个fixture返回值--是店铺的实例对象
        res = shop.query(body)
        #assert res['code'] == exp_data['code']
        ApiAssert.api_assert(res, '==', exp_data, assert_info='code',msg='店铺查询接口断言')

    @pytest.mark.skip('----暂时不运行----')
    @pytest.mark.parametrize('title,body,exp_data', get_excel_data('我的商铺', 'updateshopping'))
    @allure.story('店铺的更新')
    @allure.title('{title}')
    @pytest.mark.shop_update
    def test_shop_update(self, shop_init, title, body, exp_data):
        with allure.step('1.登录操作'):
            pass
        with allure.step('2.创建店铺实例'):
            shop = shop_init
        with allure.step('3.更新店铺的id'):
            shop_id = shop.query({'page': 1, 'limit': 20})['data']['records'][0]['id']
        with allure.step('4.更新图片信息'):
            image_info = shop.file_upload(os.path.join(data_path, '123.png'))['data']['realFileName']
        with allure.step('5.更新店铺'):
            res = shop.update(body, shop_id, image_info)
        with allure.step('6.断言'):
            assert res['code'] == exp_data['code']

if __name__ == '__main__':
    pytest.main([__file__, '-s','--alluredir', f'{report_path}', '--clean-alluredir'])
    #os.system(f'allure serve {report_path}')
