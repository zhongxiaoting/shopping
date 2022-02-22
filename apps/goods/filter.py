"""
    -*- coding: utf-8 -*-
    @Time    : 2021/5/11 8:34
    @Author  : zhongxiaoting
    @Site    : 
    @File    : filter.py
    @Software: PyCharm
"""
import django_filters
from django.db.models import Q

from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品过滤的类
    """
    # name要过滤的字段，lookup是执行的行为，小于等于本店的价格
    price_min = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte', help_text='最小价格')
    price_max = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    top_category = django_filters.NumberFilter(field_name='category', lookup_expr='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        # 不管当前是点击的是一级分类还是二级分类还是三级分类，都能找到
        return queryset.filter(Q(category_id=value) | Q(category_parent_category_id=value) |
                               Q(category_parent_category_parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'is_hot', 'is_new']
