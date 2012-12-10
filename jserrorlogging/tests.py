# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.test.utils import override_settings


def create_dummy_error_data():
    """ return dummy error data
    """
    return {
        'page': 'http://localhost?test=key',
        'url': 'http://localhost/static/app.js',
        'message': 'Uncaught ReferenceError: aaa is not defined',
        'line': 87,
        'when': 'before',
        'user_agent': ('Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.4 '
                       '(KHTML, like Gecko) Chrome/22.0.1229.92 Safari/537.4'),
    }


def create_post_data(errors, prefix='form-'):
    """ return post data
    """
    from django.forms.formsets import TOTAL_FORM_COUNT, INITIAL_FORM_COUNT
    name = prefix + '%s-%s'
    post_data = {}
    for cnt, err in enumerate(errors):
        post_data.update(dict((name % (cnt, k), v) for k, v in err.items()))
    post_data.update({
        prefix + INITIAL_FORM_COUNT: 0,
        prefix + TOTAL_FORM_COUNT: len(errors)
    })
    return post_data


def get_log_view_url():
    """ return url of log view
    """
    from django.core.urlresolvers import reverse
    return reverse('add_log')


class LogViewTests(TestCase):
    urls = 'jserrorlogging.urls'

    def test_it(self):
        data = [create_dummy_error_data()]
        res = self.client.post(get_log_view_url(), create_post_data(data))
        self.assertEqual(res.status_code, 200)
        self.assertTrue('Posted 1 errors' in res.content, res.content)

    def test_it_multiple(self):
        data = [create_dummy_error_data()]
        data.append(create_dummy_error_data())
        res = self.client.post(get_log_view_url(), create_post_data(data))
        self.assertEqual(res.status_code, 200)
        self.assertTrue('Posted 2 errors' in res.content, res.content)

    def test_it_with_meta(self):
        data = [create_dummy_error_data()]
        meta_data = [{'name': 'meta', 'value': 'dummy'}]
        post_data = create_post_data(data)
        post_data.update(create_post_data(meta_data, prefix='form0-'))
        res = self.client.post(get_log_view_url(), post_data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('Posted 1 errors' in res.content, res.content)
        from .models import Log
        log = Log.objects.get()
        self.assertEqual(
            log.meta, json.dumps(dict([(v['name'], v['value']) for v in meta_data])))

    def test_not_allowed_method(self):
        res = self.client.get(get_log_view_url())
        self.assertEqual(res.status_code, 405)

    def test_signal_save_model(self):
        data = [create_dummy_error_data()]
        self.client.post(get_log_view_url(), create_post_data(data))
        from .models import Log
        cnt = Log.objects.filter(message=data[0]['message']).count()
        self.assertEqual(1, cnt)

    @override_settings(
        JS_ERROR_NOTIFIER_MAIL_TO=[('Admin', 'admin@example.com')])
    def test_signal_notify_by_email(self):
        data = [create_dummy_error_data()]
        self.client.post(get_log_view_url(), create_post_data(data))
        # check notify
        from django.core import mail
        from django.conf import settings
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            u'%sJS_ERROR: %s' % (settings.EMAIL_SUBJECT_PREFIX, data[0]['message']))
        self.assertTrue(data[0]['message'] in mail.outbox[0].body, mail.outbox[0].body)
