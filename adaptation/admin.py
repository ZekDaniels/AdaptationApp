from django.contrib import admin
from adaptation.models import *
# Register your models here.
class AdaptationAdmin(admin.ModelAdmin):
    search_fields = ['user__profile__student_number','user__profile__namesurname']


admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(Science)
admin.site.register(Adaptation, AdaptationAdmin)
admin.site.register(StudentClass)
admin.site.register(AdapatationClass)
admin.site.register(AdaptationClassConfirmation)