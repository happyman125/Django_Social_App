# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType


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


def get_content_type_id(obj):
    """
    Function for getting content type

    :param obj: model object from which we want to get content type id
    :return: Content Type Id
    """
    return ContentType.objects.get_for_model(obj).id


def get_initials(user):
    """
    Function for getting initials from user full name of username
    If user is non authenticated, then function return symbol "A"

    :param user: user object
    :return: initials
    """
    def first(value):
        try:
            return value[0]
        except IndexError:
            return ''

    if user.is_authenticated:
        if user.get_full_name():
            return '{}{}'.format(first(user.first_name), first(user.last_name))
        return first(user.username)
    return 'A'
