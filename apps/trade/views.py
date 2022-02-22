from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializer import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from utils.permissions import IsOwnerOrReadOnly


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        查询功能
    delete：
        删除功能
        库存量-1
    create:
        增加功能
        库存量+1
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = ShopCartSerializer

    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        动态选择serializer
        :return:
        """
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    # 库存量-1
    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        # 库存 - 购物车的数量
        goods.goods_num -= shop_cart.nums
        goods.save()

    # 库存量+1
    def perform_destroy(self, instance):
        # 购物车-1
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    # 更新库存量，修改可能增加也可能减少
    def perform_update(self, serializer):
        # 获取没改变之前购物车的数量
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        # 获取现在的购物车的数量
        save_record = serializer.save()
        # 购物车改变的数量
        nums = save_record.nums - existed_nums
        # 改变库存的数量
        goods = save_record.nums
        goods.goods_num -= nums
        goods.save()

class OrderViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取个人订单
    delete：
        删除订单
    create:
        新增订单
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    # 动态分配serializer
    # 获取单个实例
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    # 获取用户的订单列表
    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        在提交订单之前还要进行两步操作，
        1、将购物车中商品的数据保存到OrderInfo中
        2、清空购物车
        :param serializer:
        :return:
        """
        order = serializer.save()  # 添加商品的保存
        # 获取购物车的所有商品
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        # 将购物车的信息赋给订单
        for shop_cart in shop_carts:
            order_goods = OrderGoods()  # 订单详情
            order_goods.goods = shop_cart.goods
            order_goods.nums = shop_cart.nums
            order_goods.order = order
            order_goods.save()  # 保存

            # 清空购物车
            shop_cart.delete()
        return order   # 返回添加的实例
