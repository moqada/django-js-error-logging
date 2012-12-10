# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models.loading import get_model
from django.template.loader import render_to_string
from .app_settings import (ENABLE_MODEL, LOG_MODEL,
                           ENABLE_EMAIL, MAIL_TO, MAIL_NOTIFY_INTERVAL)
from .signals import add_log


def save_model(sender, **kwargs):
    """ log save to model
    """
    data = kwargs.get('data')
    meta = kwargs.get('meta', None)
    model = get_model(*LOG_MODEL.split('.'))
    model.objects.save_log(data, meta=meta)


def notify_by_email(sender, **kwargs):
    """ notify by email
    """
    data = kwargs.get('data', {}).copy()
    data.update(meta=kwargs.get('meta', {}))
    cache_key = u'jserrorlogging:%(url)s:%(line)s' % data
    if cache.get(cache_key):
        return
    subject = render_to_string('jserrorlogging/email/subject.txt', dictionary=data)
    body = render_to_string('jserrorlogging/email/body.txt', dictionary=data)
    send_mail(
        u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject.strip()),
        body, settings.SERVER_EMAIL, [a for n, a in MAIL_TO])
    cache.set(cache_key, 1, MAIL_NOTIFY_INTERVAL)


if ENABLE_EMAIL:
    add_log.connect(notify_by_email)
if ENABLE_MODEL:
    add_log.connect(save_model)
