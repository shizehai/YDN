# -*- coding: utf-8 -*-
import xadmin
from xadmin import views
from .models import *
from datetime import date

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True
class GlobalSetting(object):
    site_title=u'爬虫脚本管理系统'
    site_footer=u'北京创数纪信息技术有限公司'
    menu_style='accordion'

class UserFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('decade born')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('80s', _('in the eighties')),
            ('90s', _('in the nineties')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '80s':
            return queryset.filter(birthday__gte=date(1980, 1, 1),
                                    birthday__lte=date(1989, 12, 31))

class UserProfileAdmin(object):
    # list_display=['nick_name','birthday','gender',]
    list_editable=['nick_name','birthday','gender',]
    # list_filter = (UserFilter,)

    def has_add_permission(request):
        if request.user.is_superuser:
            return True
        else:
            return False
    def has_delete_permission(request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
    def has_change_permission(request, obj=None):
        return True
    def get_queryset(self, request,model_admin):
        qs = model_admin.get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(nick_name='haia')

xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)