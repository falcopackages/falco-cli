from typing import TypeVar

from django import template
from django.db import models

register = template.Library()

_TModel = TypeVar("_TModel", bound=models.Model)


@register.filter()
def lookup(obj: _TModel) -> str:
    lookup_field = getattr(obj, "lookup_field", "pk")
    return str(getattr(obj, lookup_field))


@register.filter()
def field_verbose_names(objects, fields) -> list[str]:
    return [objects[0]._meta.get_field(f).verbose_name for f in fields]  # noqa


@register.filter(name="getattr")
def get_attribute(obj: object, field: str):
    return getattr(obj, field)


@register.filter()
def field_class_name(obj: _TModel, field: str) -> str:
    return obj._meta.get_field(field).__class__.__name__  # noqa


@register.filter
def call_get_display(obj, field_name):
    method_name = f"get_{field_name}_display"
    method = getattr(obj, method_name, None)
    if callable(method):
        return method()
