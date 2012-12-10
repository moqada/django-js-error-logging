# -*- coding: utf-8 -*-
import json
from django.db import models
from django.utils.text import Truncator
from .utils import get_browser_name


class LogManager(models.Manager):

    def save_log(self, data, meta=None):
        meta = json.dumps(meta) if meta else ''
        return self.create(meta=meta, **data)


class BaseLog(models.Model):
    created_at = models.DateTimeField()
    browser = models.CharField(max_length=50, blank=True)
    line = models.IntegerField()
    page = models.URLField(verify_exists=False)
    message = models.CharField(max_length=255)
    url = models.URLField(verify_exists=False)
    user_agent = models.CharField(max_length=255)
    when = models.CharField(max_length=50)
    meta = models.TextField(blank=True)

    objects = LogManager()

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        abstract = True

    def __unicode__(self):
        truncator = Truncator(self.message)
        return u'%s: %s' % (self.id, truncator.chars(20))

    def save(self, **kwargs):
        if not self.id:
            self.browser = get_browser_name(self.user_agent)
        return super(BaseLog, self).save(**kwargs)


class Log(BaseLog):
    pass
