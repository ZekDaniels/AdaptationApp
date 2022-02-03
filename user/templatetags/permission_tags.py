from django import template

register = template.Library()

@register.filter
def is_allowed_user(obj):
   return obj.is_allowed_user()

@register.filter
def is_allowed_simple(obj):
   return obj.is_allowed_simple()
