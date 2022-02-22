from extra_apps.DjangoUeditor.models import UEditorField
from django.db import models

# Create your models here.
from django.utils import timezone


class GoodsCategory(models.Model):
    """
    商品分类
    """
    CATEGORY_TYPE = (

        (1, "一级类目"),

        (2, "二级类目"),

        (3, "三级类目"),

    )

    name = models.CharField(max_length=30, default="", verbose_name="类别名")
    code = models.CharField(max_length=30, default="", verbose_name="类别code")
    desc = models.TextField(default="", verbose_name="类别描述")

    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别")
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="父类目级别",
                                        related_name="sub_cat")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name
        db_table = "GoodsCategory"

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    某一类下的宣传商标
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, related_name="brands", null=True, blank=True,
                                 verbose_name="商品类目")
    name = models.CharField(max_length=30, verbose_name="品牌名")
    desc = models.TextField(default="", verbose_name="名牌描述")
    image = models.ImageField(upload_to='brands/', verbose_name="图片")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "宣传广告"
        verbose_name_plural = verbose_name
        db_table = "GoodsCategoryBrand"

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name="商品类目")
    goods_sn = models.CharField(max_length=50, verbose_name="商品货号")
    name = models.CharField(max_length=100, verbose_name="商品名")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="商品销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    market_price = models.FloatField(default=0, verbose_name="市场价")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    goods_brief = models.TextField(verbose_name="商品描述")
    goods_des = UEditorField(u'商品内容', default='', width=950, height=280, imagePath="goods/images/",
                             filePath="goods/files/")
    ship_free = models.BooleanField(default=True, verbose_name="是否免运费")
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="商品封面")
    # 首页中新品展示
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    # 商品详情页的热卖商品
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品信息"
        verbose_name_plural = verbose_name
        db_table = "Goods"

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    详情页中商品的轮播图
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品", related_name="images")
    image = models.ImageField(upload_to="descriptions/", verbose_name="图片")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")


class Banner(models.Model):
    """
    商品首页轮播图
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品名")
    image = models.ImageField(upload_to="goods/banner/", verbose_name="图片")
    index = models.IntegerField(default=0, verbose_name="轮播图顺序")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "首页轮播图"
        verbose_name_plural = verbose_name
        db_table = "Banner"

    def __str__(self):
        return self.goods.name


class IndexAd(models.Model):
    """
    商品广告
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, related_name="category", verbose_name="商品类目")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='goods')

    class Meta:
        verbose_name = "首页广告"
        verbose_name_plural = verbose_name
        db_table = "IndexAd"


class HotSearchWords(models.Model):
    """
    搜索栏下方热搜词
    """
    keywords = models.CharField(max_length=100, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "热搜排行"
        verbose_name_plural = verbose_name
        db_table = "HotSearchWords"

    def __str__(self):
        return self.keywords
