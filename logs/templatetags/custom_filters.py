from django import template

register = template.Library()


@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.filter
def to_edit_url(value):
    return 'edit-'+str(value).lower()