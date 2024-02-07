import pytest
from utils.handle_excel_V3 import get_excel_data
import allure
from common.apiAssert import ApiAssert
import os
from allure_pytest import plugin as allure_plugin
from utils.handle_path import test_path


@pytest.mark.order  # 订单标签
@allure.epic('订餐系统')
@allure.feature('订单模块')  # 测试类
class Testorder(ApiAssert):
    # 1- 搜索订单
    @allure.story('订单搜索')  # 接口的名称
    @allure.title('订单搜索用例')  # 用例的标题
    @pytest.mark.order_search  # 搜索订单标签
    @pytest.mark.parametrize('title,req_body,exp_resp', get_excel_data("我的订单", "searchorder"))
    @allure.title("{title}")
    def test_search_order(self, title, req_body, exp_resp, order_init):
        # 1- 调用店铺列出接口
        # 店铺实例的创建必须要登录--需要一个店铺的实例---才能使用对应的方法
        # 调用对应的方法
        res = order_init.query(req_body)
        '''
        如果断言不是一个属性，需要多个组合判断？
        原理：assert   布尔表达式       多个条件使用and  or
        '''
        if res.get("code"):
            self.api_assert(res, '=', exp_resp, assert_info='code')
        else:
            self.api_assert(res, '=', exp_resp, assert_info='error')


if __name__ == '__main__':
    # 1- 生成报告所需的数据    --alluredir ../report/tmp
    args = [os.path.join(test_path, "test_order_manage.py"), '-s', '--alluredir', '../report/tmp']
    pytest.main(args=args, plugins=[allure_plugin])
    # pytest.main(['test_order_manage.py', '-s', '--alluredir', '../report/tmp'])  # -s 打印print信息
    # 4- 生成打开测试报告---自动打开报告的服务
    # 需要默认设置下浏览器
    os.system('allure serve ../report/tmp pause')
