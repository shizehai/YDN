# -*- coding: utf-8 -*-
from .models import *
from datetime import date
from django.contrib.admin import views
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django import forms
admin.site.site_header =u'爬虫脚本管理系统'
admin.site.site_footer=u'北京创数纪信息技术有限公司'


class UserProfileAdmin(admin.ModelAdmin):
    list_display=['user','nick_name','birthday','gender',]
    # list_editable=['nick_name','birthday','gender',]
    # list_filter = (UserFilter,)
    #
    def get_readonly_fields(self, request, obj=None):

        return ('user',)#self.readonly_fields+'user'
    def has_add_permission(self,request):
        if request.user.is_superuser:
            return True
        else:
            return False
    def has_delete_permission(self,request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
    def has_change_permission(self,request, obj=None):
        return True
    def get_queryset(self, request):
        qs = super(UserProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(UserProfile,UserProfileAdmin)
# admin.site.register(views.BaseAdminView, BaseSetting)
# admin.site.register(views.CommAdminView, GlobalSetting)
class sysProfileForm(forms.ModelForm):
    class Meta:
        model=sysProfile
        fields=['user','nick_name',]
        widgets={
            'nick_name':forms.Textarea(attrs={'cols':5,'rows':2})
        }

class sysProfileAdmin(admin.ModelAdmin):
    actions = None
    form=sysProfileForm
    list_display=['user','nick_name','birthday','gender',]
    fieldsets = [
        (None,{'fields':['user','nick_name']}),
        (u'其他设置',{'fields':['birthday','gender'],'classes':['collapse',' wide']})
    ]
    # list_editable=['nick_name','birthday','gender',]
    # list_filter = (UserFilter,)
    #
    def get_readonly_fields(self, request, obj=None):

        return ('user',)#self.readonly_fields+'user'
    def has_add_permission(self,request):
        if request.user.is_superuser:
            return True
        else:
            return False
    def has_delete_permission(self,request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
    def has_change_permission(self,request, obj=None):
        return True
    def get_queryset(self, request):
        qs = super(sysProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(sysProfile,sysProfileAdmin)