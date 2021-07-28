from django.template.defaultfilters import register


@register.filter('ellipse')
def ellipse(value):
    return value[0:3]
