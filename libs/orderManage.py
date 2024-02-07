from libs.login import Login
from common.baseApi import BaseAPI

class OrderAdmin(BaseAPI):#订单管理
    pass

if __name__ == '__main__':
    getToken = Login().login({'username': 'th0198','password': 'xintian'}, get_token=True)
    res = OrderAdmin(getToken).query({"page": "", "limit": 1})
    print(res)