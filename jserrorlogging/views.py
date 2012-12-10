# -*- coding: utf-8 -*-
import logging
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.formsets import formset_factory
from django.utils import timezone
from django.views.generic.base import TemplateView
from . import signals
from .app_settings import LOGGER_NAME, ENABLE_LOGGER
from .forms import LogForm, LogFormSet


logger = None
if ENABLE_LOGGER:
    logger = logging.getLogger(LOGGER_NAME)


class LoggingView(TemplateView):
    """ Add Log
    """
    http_method_names = ['post']
    form_class = LogForm
    form_input_name = 'value'
    formset_class = LogFormSet
    template_name = 'jserrorlogging/logging.html'

    def get_context_data(self, **kwargs):
        return kwargs

    def get_logger_message(self, data, meta=None):
        if meta:
            data = dict(meta=meta, **data)
        return json.dumps(data, cls=DjangoJSONEncoder)

    def save_log(self, data, meta_data=None):
        """ save error log
        """
        if meta_data:
            meta_data = dict([(v['name'], v['value']) for v in meta_data])
        if logger:
            logger.info(self.get_logger_message(data, meta=meta_data))
        signals.add_log.send(sender=self, data=data, meta=meta_data)

    def post(self, request, *args, **kwargs):
        now = timezone.now()
        succeeded = []
        formset = formset_factory(
            self.form_class, self.formset_class)(data=request.POST)
        for form in formset.forms:
            inline = form.inline
            if form.is_valid() and (inline is None or inline.is_valid()):
                data = form.cleaned_data.copy()
                data.update(created_at=now)
                meta_data = None if inline is None else inline.cleaned_data
                self.save_log(data, meta_data=meta_data)
                succeeded.append({'data': data, 'meta': meta_data})
        context = self.get_context_data(succeeded=succeeded)
        return self.render_to_response(context)
