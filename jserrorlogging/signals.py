# -*- coding: utf-8 -*-
import django.dispatch


add_log = django.dispatch.Signal(providing_args=['data', 'meta'])
