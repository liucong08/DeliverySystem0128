#-*- coding: utf-8 -*-
#@File    : shop.py
#@Time    : 2022/10/28 21:51
#@Author  : xintian
#@Email   : 1730588479@qq.com
#@Software: PyCharm
#Date:2022/10/28 
from common.baseApi import BaseAPI
from libs.login import Login
class Shop(BaseAPI):
    pass
    # 更新接口，不光要使用父类的update发送请求根据excel数据读取到的值
    # 额外功能：需要动态关联店铺的id  还有图片的信息
    # 总结： baseAPI父类update方法不能满足当前的店铺更新接口的需求，需要重写！
    # 问题1：每一个用例都需要更新实时正确店铺id???不需要：用例分类：正向(正常)用例/反向(异常)用例
    # 问题2：代码如何识别哪一个用例是否需要更新对应的数据(店铺的id 图片信息)：在用例加上标识
    # 问题2解决方案: ${id}
    def update(self, data=None, shop_id=None, image_info=None):
        """
        :param data: 读取到用例的数据
        :param shop_id: 实时的店铺id
        :param image_info: 实时的图片信息
        :return:
        """
        if data['id'] == '${id}':  #这个用用例的店铺id需要更新实时的id
            data['id'] = shop_id

        # 图片是否需要更新，大家去写代码 if
        data['image_path'] = image_info
        data['image'] = f'/file/getImgStream?fileName={image_info}'

        #发送请求----子类如何去调用父类的方法
        # super(子类的类名,self实例).update()
        return super(Shop,self).update(data=data)






if __name__ == '__main__':
    # 登录操作
    login_data = {'username': 'th0198', 'password': 'xintian'}
    token = Login().login(login_data, get_token=True)
    # 1.查询的测试数据
    query_data = {'page': 1, 'limit': 20}
    # 2.创建店铺实例
    shop = Shop(token)
    res = shop.query(query_data)
    shop_id = res['data']['records'][0]['id']
    # print(res)
    # 3.文件上传
    res = shop.file_upload('../data/123.png')
    print(res)
    image_info = res['data']['realFileName']

    # 4.店铺的更新接口
    update_data = {
            "name": "心田小卖部",
            "address": "上海市静安区秣陵路303号",
            "id": "999999",
            "Phone": "13176876632",
            "rating": "6.0",
            "recent_order_num":100,
            "category": "快餐便当/简餐",
            "description": "满30减5，满60减8",
            "image_path": "b8be9abc-a85f-4b5b-ab13-52f48538f96c.png",
            "image": "http://121.41.14.39:8082/file/getImgStream?fileName=b8be9abc-a85f-4b5b-ab13-52f48538f96c.png"
        }
    res = shop.update(update_data, shop_id, image_info)
    print(res)