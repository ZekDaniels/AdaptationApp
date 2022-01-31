from django import template

register = template.Library()

@register.filter
def is_confirmated_all(obj):
   return obj.get_is_confirmated_all()
