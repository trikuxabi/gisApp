from django import template

register = template.Library()

@register.filter
def luzapena_kendu(value):
    return value[:-8]