"""
    -*- coding: utf-8 -*-
    @Time    : 2021/5/9 15:13
    @Author  : zhongxiaoting
    @Site    : 
    @File    : serializers.py
    @Software: PyCharm
"""
from rest_framework import serializers

# Goods实现商品序列化
from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd


class CategorySerializer3(serializers.ModelSerializer):
    """
    三级分类
    """

    class Meta:
        model = GoodsCategory
        fileds = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    """
    二级分类
    """
    # 在parent_category字段中定义的related_name = 'sub_cat'
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    一级分类
    """
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


# 商品分类
class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


# 商品轮播图
class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = '__all__'


# 实现商品列表页
class GoodsSerializer(serializers.ModelSerializer):
    # 覆盖外键字段
    category = CategorySerializer()
    # images是数据库中设置得related_name = "images",把轮播图嵌套进来
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    """
    商品首页轮播图
    """
    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    """
    某一类下的品牌商标
    """
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexCategorySerializer(serializers.ModelSerializer):
    """
    大类下的商标
    """
    # 某一大类的商标，可以多个商标，一对多的关系
    brands = BrandSerializer(many=True)
    # goods中有一个外键categorys，但是这个外键指向的是三级类，直接反向通过外键category（三级类），取某个大类下面的商品是取不出来的
    goods = serializers.SerializerMethodField()
    # 在parent_category字段中定义的related_name = "sub_cat"
    # 取二级商品分类
    sub_cat = CategorySerializer2(many=True)
    # 广告商品
    ad_goods = serializers.SerializerMethodField()

    # goods 写方法的时候前面加‘get_’就可以得到我们想要的数据
    # 在此方法中需要调用序列化器，直接调用即可
    # 与上面的goods、ad_goods有关
    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        # 如果存在这个商品的广告
        if ad_goods:
            # 取到这个商品
            goods_ins = ad_goods[0].goods
            # 在serializer里面调用serializer的话，就要添加一个参数context。
            # serializer返回的时候一定要加“.data”，这样才是json数据
            goods_json = GoodsSerializer(goods_ins, many=True, context={'request': self.context['request']}).data
        return goods_json

    # 自定义获取方法
    def get_goods(self, obj):
        # 将这个商品相关的父类子类等都进行匹配
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'