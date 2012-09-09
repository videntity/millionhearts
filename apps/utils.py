#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.utils.datastructures import SortedDict
from django.http import Http404
from django.shortcuts import _get_queryset


def get_latest_object_or_404(klass, *args, **kwargs):
    """
    Uses get().latest() to return object, or raises a Http404 exception if
    the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.filter(*args, **kwargs).latest()
        
    except queryset.model.DoesNotExist:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)


def build_pretty_data_view(form_instance, model_object,
                           exclude=(), append=()):
    """
        Create a dictionary mapping fields with values from a model instance.
        Fields name are extracted from a form instance, then from the
        'append' iterable, and then filtered from the 'exclude' iterable.
    """
    sd = SortedDict()

    for field_name in append:
        try:
            sd[field_name] = {'label': field_name.capitalize(),
                              'fieldvalue': getattr(model_object, field_name)}
        except(AttributeError):
            pass
            # todo: are we sure we want this ? if append is filled with
            # incorrect values, this is likely going to be a bug
            # and we want the error to be loud

    for field_name, field in form_instance.fields.iteritems():

        if field_name not in exclude:
            sd[field_name] = {
                'label': field.label if field.label is not None else field_name,
                'fieldvalue': getattr(model_object, field_name)
            }

    return sd