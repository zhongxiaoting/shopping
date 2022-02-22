"""
    -*- coding: utf-8 -*-
    @Time    : 2021/5/19 23:30
    @Author  : zhongxiaoting
    @Site    : 
    @File    : serializers.py
    @Software: PyCharm
"""
from rest_framework import serializers

# 用户收藏
from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsSerializer
from user_operation.models import UserFav, UserLeavingMessage, UserAddress


class UserFavSerializer(serializers.ModelSerializer):
    # 获取当前登录的用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        # validators实现唯一联合，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                # 自定义提示信息
                message="已经收藏"
            )
        ]
        model = UserFav
        fields = ['user', 'goods', 'id']


class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    收藏商品详情
    """

    goods = GoodsSerializer

    class Meta:
        model = UserFav
        fields = ['id', 'goods']


class  UserLeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言序列化
    """
    # 获取当前的用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # 文件
    # files = serializers.FileField(write_only='message/images/')
    # 留言时间格式化; read_only:只返回，post时候可以不用提交，format：格式化输出
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')


    class Meta:
        model = UserLeavingMessage
        fields = ['user', 'message_type', 'subject', 'message', 'files', 'add_time']


class AddressSerializer(serializers.ModelSerializer):
    """
    用户收货地址序列化
    """
    # 获取当前用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # 时间
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ['id', 'user', 'provice', 'city', 'district', 'address', 'signer_name', 'add_time', 'signer_mobile']
