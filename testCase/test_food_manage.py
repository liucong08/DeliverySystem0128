import pytest
from utils.handle_excel_V3 import get_excel_data
import allure
from common.apiAssert import ApiAssert
from utils.handle_path import test_path
import os
from allure_pytest import plugin as allure_plugin
import pytest_repeat as repeat

@pytest.mark.food  # 增加标签 mark
@allure.epic('订餐系统')
@allure.feature('食品模块')  # 测试类
class TestFoodManage(ApiAssert):
    # 1- 添加食品种类
    @allure.story('添加食品种类')  # 接口的名称
    @allure.title('添加食品种类用例')  # 用例的标题
    @pytest.mark.food_add_kind  # 添加食品种类标签
    @pytest.mark.parametrize('title,req_body,exp_resp', get_excel_data('食品管理', 'Addfoodkind'))
    @allure.title("{title}")
    def test_add_food_kind(self, title, req_body, exp_resp, food_init):
        if req_body['restaurant_id'] == '3269':
            req_body['restaurant_id'] = food_init.list_food({"page": 1, "limit": 1})['data']['records'][0][
                'restaurant_id']
        res = food_init.add(req_body)
        '''
        如果断言不是一个属性，需要多个组合判断？
        原理：assert   布尔表达式       多个条件使用and  or
        '''
        if res.get("code"):
            self.api_assert(res, '=', exp_resp, assert_info='code')
        else:
            self.api_assert(res, '=', exp_resp, assert_info='error')

    #  #2- 添加食品
    @allure.story('添加食品')  # 接口的名称
    @allure.title('添加食品用例')  # 用例的标题
    @pytest.mark.food_add  # 增加食品标签
    @pytest.mark.parametrize('title,req_body,exp_resp', get_excel_data('食品管理', 'Addfood'))
    @allure.title("{title}")
    def test_add_food(self, title, req_body, exp_resp, food_init):  # 传入食品初始化条件
        res = food_init.add(req_body)
        if res.get("code"):
            self.api_assert(res, '=', exp_resp, assert_info='code')
        else:
            self.api_assert(res, '=', exp_resp, assert_info='error')

    #
    # #3- 列出食品
    @allure.story("列出食品")  # 接口的名称
    @allure.title("列出食品接口用例")  # 用例的标题
    @pytest.mark.food_list  # 列出食品标签
    @pytest.mark.parametrize('title,req_body,exp_resp', get_excel_data("食品管理", 'listfood'))
    @allure.title("{title}")
    def test_list_food(self, title, req_body, exp_resp, food_init):  # 食物的初始化条件
        res = food_init.query(req_body)
        if res.get("code"):
            self.api_assert(res, '=', exp_resp, assert_info='code')
        else:
            self.api_assert(res, '=', exp_resp, assert_info='error')

    # 4- 编辑食品
    @allure.story("编辑食品")  # 接口的名称
    @allure.title("编辑食品接口用例")  # 用例的标题
    @pytest.mark.food_update  # 修改食品标签
    @pytest.mark.parametrize('title,req_body,exp_resp', get_excel_data("食品管理", 'updatefood'))
    @allure.title("{title}")
    def test_update_food(self, title, req_body, exp_resp, update_food_init, food_init):  # 食物的初始化条件和更新的初始化条件
        if req_body['id'] == 'id':  # 判断excel的值去改成现有查询的值
            req_body['id'] = update_food_init[2]  # 更新食品id
        if req_body['idMenu'] == '3209':  # 更新菜单id
            req_body['idMenu'] = update_food_init[0]
        if req_body['idShop'] == '3269':  # 更新店铺id
            req_body['idShop'] = update_food_init[1]
        # print(inData)
        res = food_init.update(req_body)
        if res.get("code"):
            self.api_assert(res, '=', exp_resp, assert_info='code')
        else:
            self.api_assert(res, '=', exp_resp, assert_info='error')

    #
    # 5- 删除食品
    @allure.story("删除食品")
    @allure.title("删除食品接口用例")
    @pytest.mark.food_delete  # 删除食品标签
    @pytest.mark.parametrize('title,req_body,exp_resp', get_excel_data("食品管理", 'deletefood'))
    @allure.title("{caseTitle}")
    def test_delete_food(self, title, req_body, exp_resp, food_init, update_food_init):  # 传入食品初始化条件
        id = update_food_init[2]
        if req_body['id'] == 'id':
            req_body['id'] = id
        res = food_init.delete(id=req_body['id'])
        if res.get("code"):
            self.api_assert(res, '=', exp_resp, assert_info='code')
        else:
            self.api_assert(res, '=', exp_resp, assert_info='error')


if __name__ == '__main__':
    # 本地运行处理历史数据
    # 1- 生成报告所需的数据    --alluredir ../report/tmp
    args = [os.path.join(test_path, "test_food_manage.py"), '-s', '--alluredir', '../report/tmp']
    pytest.main(args=args, plugins=[allure_plugin])
    # pytest.main()  # -s 打印print信息
    # 4- 生成打开测试报告---自动打开报告的服务
    # 需要默认设置下浏览器
    os.system('allure serve ../report/tmp')
