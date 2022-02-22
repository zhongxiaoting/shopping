from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.utils import timezone


class UserProfile(AbstractUser):
    """
    用户信息
    用户登录可以是账号密码登录，也可以是手机号码登录
    """
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女')
    )

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male', verbose_name="性别")
    birthday = models.DateField(max_length=30, null=True, blank=True, verbose_name="出生年月")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    # email = models.EmailField(max_length=20, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        db_table = "UserProfile"

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    验证码
    字段：验证码，手机号码，验证码发送时间
    """
    code = models.CharField(max_length=4, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证"
        verbose_name_plural = verbose_name
        db_table = "VerifyCode"

    def __str__(self):
        return self.code



