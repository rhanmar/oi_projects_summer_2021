from typing import Iterable

from django import template
from django.core import serializers

register = template.Library()


@register.filter
def index(iter_object: Iterable, idx: int) -> object:
    """Let take element from iterable object by index."""
    return iter_object[idx]


@register.filter
def json(queryset):
    """Serialize queryset to json."""
    return serializers.serialize("json", queryset)
