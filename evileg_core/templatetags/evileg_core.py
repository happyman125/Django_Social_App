# -*- coding: utf-8 -*-

from django import template
from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static

register = template.Library()


@register.filter
def activities_count(activity_set, model_name):
    if model_name:
        return activity_set.search(model=ContentType.objects.get(model=model_name).model_class()).count()
    return activity_set.count()


@register.simple_tag
def evileg_core_css():
    return static("css/evileg_core.css")


@register.simple_tag
def evileg_core_min_css():
    return static("css/evileg_core.min.css")


@register.simple_tag
def evileg_core_js():
    return static("js/evileg_core.js")


@register.simple_tag
def evileg_core_min_js():
    return static("js/evileg_core.min.js")


@register.simple_tag
def evileg_core_popper_min_js():
    return static("js/popper.min.js")


@register.simple_tag
def evileg_core_jquery_min_js():
    return static("js/jquery-3.3.1.min.js")


@register.inclusion_tag('evileg_core/partials/object_list_preview.html', takes_context=True)
def object_list_preview(context):
    return context
