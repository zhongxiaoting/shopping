"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from goods.views import GoodsListViewSet, BannerViewSet, CategoryViewSet, IndexCategoryViewset
from trade.views import ShoppingCartViewset, OrderViewset
from users.views import UserViewset
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, AddressViewSet

router = DefaultRouter()
router.register('goods', GoodsListViewSet, basename='goods')   # 商品
router.register('categorys', CategoryViewSet, basename='categorys')  # 商品分类
router.register('users', UserViewset, basename='users')  # 用户信息
router.register('user_fav', UserFavViewSet, basename='user_fav')  # 用户收藏
router.register('user_message', UserLeavingMessageViewSet, basename='user_message')  # 用户留言
router.register('user_address', AddressViewSet, basename='user_address')  # 用户收货地址
router.register('shopping_cart', ShoppingCartViewset, basename='shopping_cart')  # 购物车
router.register('orders', OrderViewset, basename='orders')  # 订单
router.register('banners', BannerViewSet, basename='banners')  # 首页轮播图
router.register('index_goods', IndexCategoryViewset, basename='index_goods')   # 首页分类商品展示
#配置goods的url

urlpatterns = [
    path('12/', include(router.urls)),


    path('admin/', xadmin.site.urls),

    # 富文本编辑器url
    path('ueditor/', include('DjangoUeditor.urls')),
    # drf文档
    path('docs', include_docs_urls(title='优美购开发文档')),

    # rest_framework
    path('api-auth/', include('rest_framework.urls')),

    # jwt的token认证接口
    path('jwt-auth/', obtain_jwt_token),

    # token
    path('api-token-auth/', views.obtain_auth_token),

    # goods商品信息接口
    path('api/goods/', include('goods.urls', namespace='goods')),  # 商品

    # users用户登录信息接口
    path('api/users/', include('users.urls', namespace='users')),

    # 用户注册
    path('api/user_register/', UserViewset.as_view, name="user_register"),

    # 第三方登录
    path('', include('social_django.urls', namespace='social')),


]
