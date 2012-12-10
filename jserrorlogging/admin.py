# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


class LogAdmin(admin.ModelAdmin):
    """ admin for models.Log
    """
    list_display = ('id', 'message', 'browser', 'line', 'url', 'created_at')
    list_filter = ('browser',)
    ordering = ('-id',)
    readonly_fields = ('message', 'line', 'url', 'when', 'page', 'browser',
                       'user_agent', 'meta', 'created_at')
    search_fields = ('message', 'url', 'page', 'user_agent')


admin.site.register(models.Log, LogAdmin)
