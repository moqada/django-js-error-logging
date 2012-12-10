# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf.urls import patterns
from .views import LoggingView


urlpatterns = patterns(
    '',
    url(r'^add/$', LoggingView.as_view(), name='add_log'),
)
