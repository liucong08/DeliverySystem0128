# -*- coding: utf-8 -*-
# @File    : encrypt_data.py
# @Time    : 2022/10/26 20:54
# @Author  : xintian
# @Email   : 1730588479@qq.com
# @Software: PyCharm
# Date:2022/10/26
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import base64
from utils.handle_path import public_path

"""
加密算法分类：
    - md5系列加密  哈希算法类型
    - aes加密  对称加密  加密/解密是一个密钥
    - rsa加密  非对称加密，加密/解密使用一对公私钥-----安全系数相对高些
    - sm4加密   国密
"""


def get_md5_data(data: str, salt=''):
    """
    :param data: 被加密的数据
    :param salt: 盐值，默认是空
    :return: 返回加密得到的16进制数据的密文
    """
    # 1.创建md5实例
    md5 = hashlib.md5()
    data = f'{data}{salt}'  # data = data+salt
    # 2.调用加密函数md5.update()
    md5.update(data.encode('utf-8'))
    # 3.返回加密的密文
    return md5.hexdigest()


"""
RSA加密的代码编辑：
    1- 安装对应的库 cmd---pip install pycryptodome
    2- rsa加密处理流程：
        - 1.先获取/加密公钥文件
        - 2.输入需要加密的明文数据---加密函数一定有一个形参data
        - 3.把输入的字符串---byte  str:'abc'-----b‘abc’
        - 4.使用加密方法加密
        - 5.使用base64编码（加密的密文进行编码）
        - 6.解码---密文是bytes字节码---dencode()-----字符串
"""


class RsaEndecrypt:
    """Rsa的类"""

    def __init__(self, file_path=public_path):
        self.file_path = file_path

    def encrypt(self, crypt_data):
        # 1.先获取/加密公钥文件---公钥数据
        with open(f'{self.file_path}\public.pem', 'rb') as fo:
            # 2.获取公钥的内容
            key_content_bytes = fo.read()
            # 3.把输入的明文密码--bytes
            crypt_data = crypt_data.encode('utf-8')
            # 4. 需要把公钥的内容给对应函数---RSA公钥对象
            public_key = RSA.importKey(key_content_bytes)
            # 5.使用公钥对象，生成一个加密对象  cipher
            cipher = PKCS1_cipher.new(public_key)
            # 6.调用加密方法encrypt(必须是bytes数据)
            encrypt_text = cipher.encrypt(crypt_data)
            # 7.使用base64编码---解码--字符串
            return base64.b64encode(encrypt_text).decode('utf-8')


if __name__ == '__main__':
    res = RsaEndecrypt().encrypt('123456')
    print(res)
