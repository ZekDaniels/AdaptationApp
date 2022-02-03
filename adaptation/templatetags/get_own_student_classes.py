from django import template
register = template.Library()

@register.filter
def get_own_student_classes(obj, adaptation):
   return obj.get_own_student_classes(adaptation).order_by("adaptation_class")


@register.filter
def get_own_student_classes_count(obj, adaptation):
   return obj.get_own_student_classes(adaptation).count()

@register.filter
def get_adaptation_class_list_akts_sum(obj):
   return obj.get_adaptation_class_list_akts_sum()