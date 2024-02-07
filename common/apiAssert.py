#-*- coding: utf-8 -*-
#@File    : apiAssert.py
#@Time    : 2022/11/7 21:52
#@Author  : xintian
#@Email   : 1730588479@qq.com
#@Software: PyCharm
#Date:2022/11/7 
# 封装断言意义： 更好定位问题，让报错信息可以日志或allure提醒
#断言分类： ==  != in not equal >  <
from utils.handle_loguru import log
import traceback
class ApiAssert:
    """ 断言类，不需要创建实例"""
    @classmethod  # 类方法
    def api_assert(cls, result, condition, exp_result, assert_info, msg='断言操作'):
        assert_detail= '实际结果:{0},预期结果:{1}'
        """
        :param result:  实际返回数据
        :param condition: 判断条件
        :param exp_result: 预期的返回数据
        :param assert_info: 断言的关键信息  code   msg
        :param msg: 操作描述
        :return: 断言结果
        """
        try:
            assert_type = {
                "==": result[assert_info] == exp_result[assert_info],
                "!=": result[assert_info] != exp_result[assert_info],
                "in": result[assert_info] in exp_result[assert_info] if  isinstance(exp_result[assert_info],list) else  False ,
            }
            if condition in assert_type:  # 当前的断言条件在我们规划 的断言类型里
                assert assert_type[condition]
                # assert res['msg'] == resp_exp['msg']
            else:
                AssertionError("你输入的断言类型，不在规划里面，请检查断言条件！")
                #断言操作记录到日志文件里
            log.info(f'{msg},断言类型:{condition},断言详情：{assert_detail.format(result[assert_info],exp_result[assert_info])}')
        except Exception as error:
            log.error(traceback.format_exc())
            raise error
            # 打印日志

