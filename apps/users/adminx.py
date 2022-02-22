from django.contrib import admin

# Register your models here.
import xadmin
from users.models import VerifyCode


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', 'add_time']


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
