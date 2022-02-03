from django import template
register = template.Library()

@register.filter
def get_own_student_classes(obj, adaptation):
   return obj.get_own_student_classes(adaptation).count()
