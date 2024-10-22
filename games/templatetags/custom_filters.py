from django import template

register = template.Library()


@register.filter
def range_filter(start, end):
    return range(start, end)


@register.filter
def index(List, i):
    return List[int(i)]
