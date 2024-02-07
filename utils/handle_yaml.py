# -*- coding: utf-8 -*-
# @File    : handle_yaml.py
# @Time    : 2022/10/30 10:10
# @Author  : xintian
# @Email   : 1730588479@qq.com
# @Software: PyCharm
# Date:2022/10/30
import yaml
import os.path


# yaml文件嵌套yaml文件
class Loader(yaml.Loader):  # 继承
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


Loader.add_constructor('!include', Loader.include)


def get_yml_data(file_path: str):
    with open(file_path, encoding='utf-8') as fo:  # file object
        # 把读取到的字符串转化为python好操作的字典与列表之类的了类型
        return yaml.safe_load(fo.read())


def get_case_data(file_path: str):
    res_list = []
    res = get_yml_data(file_path)
    for one in res:
        res_list.append((one['detail'], one['data'], one['resp']))
    return res_list


if __name__ == '__main__':
    res = get_case_data('../data/loginCase.yml')
    print(res)
