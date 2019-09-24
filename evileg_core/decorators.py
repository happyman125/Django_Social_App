# -*- coding: utf-8 -*-

from functools import wraps, partial

import requests
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _


def recaptcha(function):
    """
    Google recaptcha decorator. It can be used against robots and brute force.


    :param function: wrapped view function, which should be checked via Google recaptcha
    :return: wrapped function
    """
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.user.is_authenticated:
            request.recaptcha_is_valid = True
            return function(request, *args, **kwargs)

        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, _('Invalid reCAPTCHA. Please try again.'))
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def model_cached_property(function=None, timeout=getattr(settings, "MODEL_CACHED_PROPERTY_TIMEOUT", 60)):
    """
    Decorator for caching expensive properties in django models

    WARNING:
    This decorator doesn`t work with dynamic objects in function arguments,
    For example it doesn`t work with AnonymousUser, only with authenticated User

    :param timeout: cache timeout
    :param function: wrapped function, which should be cached
    :return: wrapped function
    """
    if function is None:
        return partial(model_cached_property, timeout=timeout)

    @wraps(function)
    def function_wrapper(model_object, *args, **kwargs):
        cache_key = 'evileg_core_model_cached_property_{}_{}_{}_{}_'.format(
            model_object._meta.db_table, model_object.id, function.__name__,
            "{} {}".format(args, kwargs).replace(" ", "_")
        )
        result = cache.get(cache_key)
        if result is not None:
            return result
        result = function(model_object, *args, **kwargs)
        cache.set(cache_key, result, timeout=timeout)
        return result

    return function_wrapper
