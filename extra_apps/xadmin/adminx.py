from __future__ import absolute_import
import xadmin
from .models import UserSettings, Log
from xadmin.layout import *
from . import views
from django.utils.translation import ugettext_lazy as _, ugettext


class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True


xadmin.site.register(UserSettings, UserSettingsAdmin)


class LogAdmin(object):

    def link(self, instance):
        if instance.content_type and instance.object_id and instance.action_flag != 'delete':
            admin_url = self.get_admin_url(
                '%s_%s_change' % (instance.content_type.app_label, instance.content_type.model),
                instance.object_id)
            return "<a href='%s'>%s</a>" % (admin_url, _('Admin Object'))
        else:
            return ''

    link.short_description = ""
    link.allow_tags = True
    link.is_column = False

    list_display = ('action_time', 'user', 'ip_addr', '__str__', 'link')
    list_filter = ['user', 'action_time']
    search_fields = ['ip_addr', 'message']
    model_icon = 'fa fa-cog'


xadmin.site.register(Log, LogAdmin)


# X admin的全局配置信息设置
class BaseSetting(object):
    # 主题功能开启
    enable_themes = True
    use_bootswatch = True


# 将xadmin全局管理器与我们的view绑定注册
xadmin.site.register(views.BaseAdminView, BaseSetting)


# x admin 全局配置参数信息设置
class GlobalSettings(object):
    site_title = '优美购管理后台'
    site_footer = '优美购科技有限公司'
    # 收起菜单
    menu_style = 'accordion'


# 将头部与脚部信息进行注册
xadmin.site.register(views.CommAdminView, GlobalSettings)
