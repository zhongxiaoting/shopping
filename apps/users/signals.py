"""
    -*- coding: utf-8 -*-
    @Time    : 2021/5/18 23:23
    @Author  : zhongxiaoting
    @Site    : 
    @File    : signals.py
    @Software: PyCharm
"""
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


# 用信号量实现加密
# post_save：接收信号的方式，send：接收信号的模型
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    # 判断是否新建
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
    return instance