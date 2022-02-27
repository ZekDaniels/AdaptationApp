from django.contrib import admin
from user.forms import ProfileAdminForm
from user.models import Profile
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):

    form = ProfileAdminForm
    

admin.site.register(Profile, ProfileAdmin)