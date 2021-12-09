from django import template

register = template.Library()

@register.filter
def get_max_grade(obj):
   return obj.get_max_grade()
