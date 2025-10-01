from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply two numbers"""
    return value * arg
