"""
    -*- coding: utf-8 -*-
    @Time    : 2021/5/20 10:37
    @Author  : zhongxiaoting
    @Site    : 
    @File    : permissions.py
    @Software: PyCharm
"""

# 权限验证
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user