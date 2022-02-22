"""
    -*- coding: utf-8 -*-
    @Time    : 2021/6/1 16:04
    @Author  : zhongxiaoting
    @Site    : 
    @File    : signal.py
    @Software: PyCharm
"""

# 信号量实现用户收藏的+1和-1
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user_operation.models import UserFav


# post_save:接收信号的方式
# sender:接收信号的model
@receiver(post_save, sender=UserFav)
def create_UserFav(sender, instance=None, created=False, **kwargs):
    """
    是否新建，update的时候也会进行post_save
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_UserFav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
