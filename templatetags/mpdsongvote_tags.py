from django import template
register = template.Library()


@register.filter(name="divmod")
def divmod_filter(value, arg):
    return divmod(int(value), int(arg))


@register.filter(name="zfill")
def zfill_filter(value, arg):
    return str(value).zfill(arg)


@register.filter(name="title_from_filename")
def title_from_filename_filter(value):
    # remove path
    filename = value.split("/")[-1]
    # remove file extension
    parts = filename.split(".")
    if len(parts) == 1:
        return parts[0]
    else:
        return ".".join(parts[:-1])
