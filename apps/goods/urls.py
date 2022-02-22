"""
    -*- coding: utf-8 -*-
    @Time    : 2021/5/9 15:45
    @Author  : zhongxiaoting
    @Site    : 
    @File    : urls.py
    @Software: PyCharm
"""
from django.urls import path

from goods.views import GoodsListViewSet, CategoryViewSet

app_name = 'goods'
urlpatterns = [
    # 商品的列表信息
    # path('goods_list/', GoodsListViewSet.as_view({'get': 'get'}), name='goods_list'),

    # 商品的目录信息
    # path('goods_category/', CategoryViewSet.as_view(), name='goods_category'),

]

