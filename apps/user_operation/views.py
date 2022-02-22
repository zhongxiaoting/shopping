from django.shortcuts import render

# Create your views here.

# 实现商品收藏的增删改查
from rest_framework import viewsets
from rest_framework import mixins

from goods.views import OwnerPagination
from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, UserLeavingMessageSerializer, \
    AddressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(viewsets.ModelViewSet):
    """
    用户收藏：添加、删除、查找
    """
    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    # 权限验证,IsAuthenticated：必须是登录用户；IsOwnerOrReadOnly:必须是当前登录的用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # auth做用户验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 搜索的字段
    lookup_field = 'goods_id'

    # 动态选择serializer
    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavSerializer

    def get_queryset(self):
        # 只看到当前用户的收藏
        return UserFav.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        用户收藏商品数量+1
        :param serializer:
        :return:
        """
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


# 用户留言的查看，添加，删除
class UserLeavingMessageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                                mixins.DestroyModelMixin):
    """
    List:
        获取用户留言
    create:
        添加用户留言
    Destroy:
        删除用户留言
    """
    # 分页
    pagination_class = OwnerPagination
    # 序列化类
    serializer_class = UserLeavingMessageSerializer
    # 权限验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 用户验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 用户只能看到自己的留言
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


# 用户收货地址的增删改查
class AddressViewSet(viewsets.ModelViewSet):
    """
    list:
        查看收货地址
    create:
        添加收货地址
    delete：
        删除收货地址
    update:
        修改收货地址
    """

    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 作者自己可见
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
