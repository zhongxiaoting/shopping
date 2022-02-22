"""
    -*- coding: utf-8 -*-
    @Time    : 2021/5/12 21:13
    @Author  : zhongxiaoting
    @Site    : 
    @File    : urls.py
    @Software: PyCharm
"""
from django.urls import path

from users.views import SmsCodeViewSet, UserViewset

app_name = 'users'

urlpatterns = [
    # 发送验证码
    # path('send_code/', SmsCodeViewSet.as_view(), name="send_code"),



]