"""
    -*- coding: utf-8 -*-
    @Time    : 2021/5/29 19:25
    @Author  : zhongxiaoting
    @Site    : 
    @File    : serializer.py
    @Software: PyCharm
"""
import time
from random import Random

from rest_framework import serializers

from goods.models import Goods
from goods.serializers import GoodsSerializer
from trade.models import ShoppingCart, OrderGoods, OrderInfo


class ShopCartDetailSerializer(serializers.ModelSerializer):
    """
    购物车商品的详情
    """
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['goods', 'nums']


class ShopCartSerializer(serializers.Serializer):
    """
    添加购物车
    """
    # 获取用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, label="数量", min_value=1, error_messages={
        "min_value": "商品数量不能小于1"
    })

    # 获取商品名称，goods是一个外键，可以通过这方法获取goods object中的所有值
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    # 继承Serializer没有create、update方法。
    def create(self, validated_data):
        user = self.context['request'].user  # 获取用户
        nums = validated_data['nums']
        goods = validated_data['goods']

        # 如果购物车里有这个商品就数量+1，没有就新添加
        existed = ShoppingCart.objects.filter(goods=goods, user=user)
        if existed:
            existed = existed[0]
            print(existed)
            existed.nums += nums
            existed.save()
        # 没有就创建
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    # 更改购物车数量
    def update(self, instance, validated_data):
        # 修改购物车数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderGoodSerializer(serializers.ModelSerializer):
    """
    订单中的商品
    """
    goods = GoodsSerializer

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    订单商品信息详情
    """
    goods = OrderGoodSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    订单商品信息
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    nonce_str = serializers.CharField(read_only=True)
    pay_type = serializers.CharField(read_only=True)

    def generate_order_sn(self):
        """
        生成订单号
        :return:
        """
        random_ins = Random()
        order_sn = "{time_str}{user_id}{ran_str}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                         user_id=self.context["request"].user.id,
                                                         ran_str=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        # validate中添加order_sn, 然后再view中就可以save
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
