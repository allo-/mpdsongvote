from django import template
from mpdsongvote.util import title_from_filename
register = template.Library()


@register.filter(name="divmod")
def divmod_filter(value, arg):
    return divmod(int(value), int(arg))


@register.filter(name="zfill")
def zfill_filter(value, arg):
    return str(value).zfill(arg)


register.filter('title_from_filename', title_from_filename)
