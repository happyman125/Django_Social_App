# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.db import models

from .utils import EMarkdownWorker
from .widgets import EMarkdownWidget


class EMarkdownField(models.TextField):
    class EMarkdownProxy:
        def __init__(self, field):
            self.field = field

        def __get__(self, obj, model):
            if obj is None:
                return self.field

            value = obj.__dict__[self.field.name]
            return value

        def __set__(self, obj, value):
            obj.__dict__[self.field.name] = value
            if value and len(value) > 0:
                languages = getattr(settings, "LANGUAGES", None)
                if 'modeltranslation' in settings.INSTALLED_APPS and self.field.name.endswith(
                        tuple([code for code, language in languages])):
                    obj.__dict__['{}_{}'.format(self.field.html_field, self.field.name[-2:])] = EMarkdownWorker(
                        value).get_text()
                else:
                    obj.__dict__[self.field.html_field] = EMarkdownWorker(value).get_text()

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, name, EMarkdownField.EMarkdownProxy(self))

    def __init__(self, html_field=None, *args, **kwargs):
        self.html_field = html_field
        self.placeholder = kwargs.pop("placeholder", '')
        self.upload_link = kwargs.pop("upload_link", None)
        if not self.upload_link:
            self.upload_link = getattr(settings, 'MARKDOWN_UPLOAD_LINK', None)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self._get_form_class(),
            'documentation_link': getattr(settings, "MARKDOWN_DOCUMENTATION_LINK", None),
            'placeholder': self.placeholder,
            'upload_link': self.upload_link,
        }
        defaults.update(**kwargs)
        return super().formfield(**defaults)

    @staticmethod
    def _get_form_class():
        return EMarkdownFormField


class EMarkdownFormField(forms.fields.CharField):

    def __init__(self, documentation_link=None, placeholder=None, upload_link=None, *args, **kwargs):
        kwargs.update({'widget': EMarkdownWidget(
            documentation_link=documentation_link,
            placeholder=placeholder,
            upload_link=upload_link
        )})
        super().__init__(*args, **kwargs)
