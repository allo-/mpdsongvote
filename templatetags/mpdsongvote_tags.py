from django import template
register = template.Library()


@register.filter(name="divmod")
def divmod_filter(value, arg):
    return divmod(int(value), int(arg))


@register.filter(name="zfill")
def zfill_filter(value, arg):
    return str(value).zfill(arg)
