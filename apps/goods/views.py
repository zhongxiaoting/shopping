from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, generics, filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework.views import APIView

from goods.filter import GoodsFilter
from goods.models import Goods, GoodsCategory, Banner
from goods.serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class OwnerPagination(PageNumberPagination):
    """
    自定义分页功能
    """
    # 显示每页显示的页数
    page_size = 5
    # 可以动态的改变每页显示的页数
    page_size_query_param = "page_size"
    # 页码参数
    page_query_param = "page"
    # 最多能显示多少页
    max_page_size = 100


# CacheResponseMixin要放在第一位，这是基于内存的缓存，重启之后就丢失
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    list:
        商品列表页
    retrieve:
        商品详情页
    """
    pagination_class = OwnerPagination  # 分页
    queryset = Goods.objects.all().order_by("id")
    serializer_class = GoodsSerializer
    throttle_classes = (UserRateThrottle, AnonRateThrottle)  # 限制访问的速率

    # 设置filter类为自定义的类
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter

    # 搜索=name表示精准搜索
    search_fields = ['name', 'goods_brief', 'goods_desc']
    # 排序
    ordering_fields = ['sold_num', 'shop_price']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # 商品点击数+1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    列出商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页轮播图
    """
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    # 获取is_tab = True （导航栏）里面的分类下的商品数据
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品', '酒水饮料'])
    serializer_class = IndexCategorySerializer
