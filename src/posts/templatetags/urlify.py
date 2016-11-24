from urllib.parse import quote_plus
from django import template

register = template.Library()


@register.filter
# This takes text and turns it into URL format
def urlify(value):
    return quote_plus(value)

