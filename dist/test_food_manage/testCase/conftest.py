#-*- coding: utf-8 -*-
#@File    : conftest.py
#@Time    : 2022/11/4 21:37
#@Author  : xintian
#@Email   : 1730588479@qq.com
#@Software: PyCharm
#Date:2022/11/4 
import pytest
from configs.conf import NAME_PWD
from libs.foodManage import FoodManage
from libs.login import Login
from libs.orderManage import OrderAdmin
from libs.shop import Shop
from utils.handle_mongo import MongoConnection
# @pytest.fixture(scope='class', autouse=True, params=['第1次运行>>>','第2次运行>>>'])
# def start_running(request):
#     print(f'{request.param}')
#     yield
#     print('这里可以写数据清除的代码')


# 登录操作的初始化操作
@pytest.fixture(scope='session')
def login_init():
    print('---用户登录操作---')
    # 登录操作
    token = Login().login(NAME_PWD, get_token=True)
    yield token #有返回值的作用
    print('---退出操作---')

# 创建店铺的实例操作
# 技术点1：不同 fixture可以相互调用，下一个fixture函数定义时候，参数写上一个fixture函数名,已经关联上了
# 技术点2：如何使用 上一个fixture的返回值，下一个fixtire函数里面直接使用上一个fixture函数名就是它的返回值
@pytest.fixture(scope='session')
def shop_init(login_init):
    print('---创建店铺实例---')
    # 2. 传递token--创建店铺实例
    shop = Shop(login_init)
    yield shop

#3- 食品的实例化，初始化条件
@pytest.fixture(scope='class')
def food_init(login_init):#
    food= FoodManage(login_init)#先登录创建一个实例
    print('---正在操作食品初始化---')
    #添加食品
    food.add({"name":"炸鸡","idShop":9441,"category_id":38393,"attributesJson":["新"],"specsJson":[{"specs":"默认","packing_fee":0,"price":20}]})
    return food
#-----店铺更新初始化操作
@pytest.fixture(scope='class')
def shop_update_init(shop_init):

    shop_object = shop_init
    shop_id = shop_init.query({'page': 1, 'limit': 20})['data']['records'][0]['id']
    image_info = shop_init.file_upload('../data/123.png')['data']['realFileName']
    shop_update = {'shop_object':shop_object,'shop_id':shop_id,'image_info':image_info}
    #yield shop_object,shop_id,image_info#元组
    yield shop_update#字典

"""
在使用 pytest.mark.parametrize 对用例进行参数化的时候，传入的值包含中文，运行用例，控制台显示编码问题。
解决方法：在用例的根目录下，新建 conftest.py文件，将下面的代码复制进去
"""
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")

@pytest.fixture(scope='function')
def update_food_init(food_init):
    #菜单id
    idMenu = food_init.query({"page": 1, "limit": 1})['data']['records'][0]['category_id']
    #店铺id
    shopid = food_init.query({"page": 1, "limit": 1})['data']['records'][0]['restaurant_id']
    #食品id
    foodid = food_init.query({"page": 1, "limit": 1})['data']['records'][0]['item_id']
    print('正在执行---update_food_init---')
    return idMenu,shopid,foodid


#4- 订单的实例化，初始化条件
@pytest.fixture(scope='class')
def order_init(login_init):#
    order= OrderAdmin(login_init)#先登录创建一个实例
    print('---正在操作食品初始化---')
    return order


#5- 退出操作
@pytest.fixture(scope='class')
def user_logout(login_init):#
    loginObject= Login()
    #退出操作
    loginObject.logout(login_init)



#mongodb操作
@pytest.fixture(scope='class')
def food_db_init(shop_init):
    shopid=shop_init[0]
    db=MongoConnection()
    res=db.find('foods',{'restaurant_id':shopid})
    for one in res:
        print(one)

    db.delete('foods',{'restaurant_id':shopid},many=True)
    res2=db.find_one('foods',{'restaurant_id':shopid})
    if res2 ==None:
        print('食品清空完毕')

    print('添加食品操作')
    db.insert('foods',{'restaurant_id':shopid,"category_id":3333,"description":'非常好吃',"item_id":6872,'name':'烤肉饭'})
    res=db.find('foods',{"item_id":6872})