from libs.login import Login
from libs.shop import Shop
import json
from common.baseApi import BaseAPI
import pprint
class FoodManage(BaseAPI):

    def category_list(self,id):
        """
        食品详细信息
        :param id: 商铺id
        :return: 响应
        """
        return self.request_send(id=id)
    def add(self,inData):
        #需要修改参数格式重写数据并调用父类方法
        if inData.get('attributesJson'):
                inData['attributesJson']=json.dumps(inData['attributesJson'])
        if inData.get('specsJson'):
            inData['specsJson'] = json.dumps(inData['specsJson'])
        return super(FoodManage, self).add(data=inData)

    def update(self,inData):
        # 需要修改参数格式重写数据并调用父类方法
        inData['specsJson'] = json.dumps(inData['specsJson'])
        return super(FoodManage, self).update(data=inData)
if __name__ == '__main__':
    #1- 登录成功
    token = Login().login({"username":"ka0181","password":"26205"},get_token=True)
    # res=FoodManage(token).query({'page':1,'limit':20})
    # print(res)
    resp=FoodManage(token).category_list(9441)['category_list'][0]['id']
    print(resp)
    #2- 列出商铺--id
    res=FoodManage(token).query({'page':1,'limit':20})
    pprint.pprint(res)
    id=FoodManage(token).query({"page": 1, "limit": 1})['data']['records'][-1]['item_id']
    print(id)
    res=FoodManage(token).query({"page": 1, "limit": 20})
    print(res)
    #3- 获取食品的id
    print(res['data']['records'][0]['item_id'])
    shopid=Shop(token).query({"page":1,"limit":20})['data']['records'][0]['id']
    category_id=FoodManage(token).category_list(shopid)['category_list'][0]['id']
    res=FoodManage(token).add({"name":"炸鸡","idShop":shopid,"category_id":category_id,"attributesJson":["新"],"specsJson":[{"specs":"默认","packing_fee":0,"price":20}]})