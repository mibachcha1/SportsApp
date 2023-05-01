from django import template

register = template.Library()

@register.filter
def mins(value):
    return value[2:4]

@register.filter
def percent(value):
    percent = "{:.0%}".format(value)
    return percent

