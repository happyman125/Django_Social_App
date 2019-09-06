# -*- coding: utf-8 -*-

from django.core.cache import cache


def cache_invalidate_cached_property(model_object, function):
    """
    Receiver for invalidating cached property

    :param model_object: model instance, on which should be invalidated property
    :param function: wrapped function, which should be invalidated
    :return:
    """
    cache_key = 'evileg_core_cached_property_{}_{}_{}_'.format(
        model_object._meta.db_table, model_object.id, function.__name__
    )
    cache.delete(cache_key)
