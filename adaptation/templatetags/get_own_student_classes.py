from django import template
register = template.Library()

@register.filter
def get_own_student_classes(obj, adaptation):
   return obj.get_own_student_classes(adaptation).order_by("adaptation_class")


@register.filter
def get_own_student_classes_count(obj, adaptation):
   return obj.get_own_student_classes(adaptation).count()
