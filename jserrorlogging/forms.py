# -*- coding: utf-8 -*-
from django import forms
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory


class LogForm(forms.Form):
    """ form for save log
    """
    message = forms.CharField()
    line = forms.IntegerField()
    page = forms.URLField()
    url = forms.URLField()
    user_agent = forms.CharField()
    when = forms.CharField()


class MetaLogForm(forms.Form):
    """ form for meta data
    """
    name = forms.CharField()
    value = forms.CharField(required=False)


class LogFormSet(BaseFormSet):

    def _construct_form(self, i, **kwargs):
        form = super(LogFormSet, self)._construct_form(i, **kwargs)
        inline = formset_factory(MetaLogForm, extra=0)
        try:
            form.inline = inline(data=self.data, prefix=u'%s%s' % (self.prefix, i))
        except forms.ValidationError:
            form.inline = None
        return form
