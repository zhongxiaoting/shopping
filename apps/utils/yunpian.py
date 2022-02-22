"""
    -*- coding: utf-8 -*-
    @Time    : 2021/5/12 21:05
    @Author  : zhongxiaoting
    @Site    : 
    @File    : yunpian.py
    @Software: PyCharm
"""
import json

import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"


    def send_sms(self, code, mobile):
        # 需要传递的参数
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【优美购生鲜超市】您的验证码是{code}，1分钟内有效。若非本人操作，请忽略本短信".format(code=code)
        }

        response = requests.post(self.single_send_url)
        re_dict = json.loads(response.text)
        return re_dict

if __name__ == "__main__":
    yun_pian = YunPian("2e87d17327d4be01608f7c6da23ecea2")
    yun_pian.send_sms("2021", "手机号码")