from django import template

register = template.Library()

@register.filter(name='length_is')
def length_is(value, arg):
    return len(value) == int(arg)

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={"class": css_class})