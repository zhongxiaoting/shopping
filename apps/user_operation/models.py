from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.utils import timezone

from goods.models import Goods

User = get_user_model()


class UserFav(models.Model):
    """
    用户收藏操作
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品名")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")  # 联合约束

    def __str__(self):
        return self.user.usename


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    provice = models.CharField(max_length=100, verbose_name="省份")
    city = models.CharField(max_length=100, verbose_name="城市")
    district = models.CharField(max_length=100, verbose_name="区域")
    address = models.CharField(max_length=100, default="", verbose_name="详细地址")
    signer_name = models.CharField(max_length=100, verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="电话")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name
        db_table = "UserAddress"

    def __str__(self):
        return self.address


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]  # 后缀
    dt = datetime.now()
    filename = 'message/files/{0}.{1}'.format(dt.strftime('%Y-%m-%d-%H-%M'), ext)
    return filename


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型")
    subject = models.CharField(max_length=256, verbose_name="主题", null=True, blank=True)
    message = models.TextField(null=True, blank=True, verbose_name="留言内容")
    file = models.FileField(upload_to=user_directory_path, verbose_name="上传文件")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name
        db_table = "UserLeavingMessage"

    def __str__(self):
        return self.subject
