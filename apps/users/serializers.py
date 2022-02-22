"""
    -*- coding: utf-8 -*-
    @Time    : 2021/5/12 19:54
    @Author  : zhongxiaoting
    @Site    : 
    @File    : serializers.py
    @Software: PyCharm
"""

import re
from datetime import timedelta, datetime

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from shopping.settings import REGEX_MOBILE
from users.models import VerifyCode

User = get_user_model()

# 短信序列化
class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        手机号码验证
        :param mobile:
        :return:
        """

        # 是否已经验证
        if User.objects.filter(mobile=mobile):
            raise serializers.ValidationError("用户已经存在")

        # 是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不正确")

        # 1分钟内只能发送一次
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile):
            raise serializers.ValidationError("距离上次发送还未到一分钟")
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册
    """
    # UserProfile中没有code字段，需要自己定义一个，5分钟之后自动删除
    code = serializers.CharField(required=True, write_only=True, allow_blank=False, max_length=4, min_length=4,label="验证码",
    error_messages = {
        "blank": "请输入验证码",
        "required": "请输入验证码",
        "max_length": "验证码格式错误",
        "min_length": "验证码格式错误",
    })
    # 验证用户名是否存在，required必填, validators有效性检查
    username = serializers.CharField(label="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(style={'input_type': 'password'}, label=True, write_only=True)

    # 密码加密
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user





    # 验证code
    def validated_data(self, code):
        # 用户注册，post数据都保存在initial_data里面
        # username就是验证的手机号，验证码按照添加的时间倒序排序，为了后面验证码的过期，错误等
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username'].order_by['-add_time'])

        if verify_records:
            # 获取最近的一个验证码
            last_code = verify_records[0]
            # 设置有限期为5分钟
            five_mintes_ago = datetime.time() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_code.add_time:
                # 如果验证码过期就删除
                del last_code.code
                raise serializers.ValidationError("验证码过期")

            if last_code.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    # 所有字段, attrs是字段验证合法之后返回的总dict
    def validate(self, attrs):
        # 在手机号码验证正确时保存手机号码
        attrs["mobile"] = attrs["username"]

        # code是自己临时添加的，数据库中并没有这个字段，验证完之后删除
        del attrs['code']
        # 返回所有的字段
        return attrs


    class Meta:
        model = User
        fields = ['username', 'code', 'mobile', 'password']


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """
    class Meta:
        model = User
        fields = ['name', 'gender', 'birthday', 'email', 'mobile']






