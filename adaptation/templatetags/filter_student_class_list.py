from django import template
register = template.Library()

@register.filter
def filter_student_class_list(classes, semester):
   return classes.filter(semester=semester)
