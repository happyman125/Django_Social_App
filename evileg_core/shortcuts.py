# -*- coding: utf-8 -*-


def get_object_or_none(klass, *args, **kwargs):
    """
    Use get() to return an object or None raise if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.

    :param klass: Model, Manager, or QuerySet object
    :param args: arguments are used in the get() query
    :param kwargs: keyword arguments are used in the get() query
    :return: Object or None
    """
    try:
        return klass._default_manager.get(*args, **kwargs)
    except klass.DoesNotExist:
        return None