from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, permissions
# Create your views here.

from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from shopping.settings import APIKEY
from users.serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian

User = get_user_model()

# 自定义用户名和手机号码登录
from users.models import UserProfile, VerifyCode


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 发送短信
class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    手机验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字验证码
        :return:
        """

        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(i)

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 验证合法性
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        # 发送短信
        yun_pian = YunPian(APIKEY)

        # 生成验证码
        code = self.generate_code()

        # 发送短信
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户注册
    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 动态权限分配
    #
    def get_permissions(self):
        """
        用户注册时不应该有权限限制;获取用户详情信息的时候必须登录
        :return:
        """
        # 详情
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated]
        # 注册用户
        elif self.action == 'create':
            return []
        return []

    # 动态选择序列化方式
    def get_serializer_class(self):
        """
        1、UserRegSerializer（用户注册），只返回username和mobile，用户详情返回更多的字段
        2、如果注册的时候使用userdetailSerializer，会导致验证失败，所以需要动态选择
        :return:
        """
        if self.action == 'retrieve':
            # 用户详情
            return UserDetailSerializer
        elif self.action == 'create':
            # 用户注册
            return UserRegSerializer
        return UserDetailSerializer

    # 重写get_object()
    def get_object(self):
        """确定用户id"""
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
