from django.contrib import admin
#
# # Register your models here.
# from .models import UserProfile
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','nickname','email','gender','age']
    list_filter = ['gender']
    list_editable = ['nickname','gender','age']

#
# admin.site.register(UserProfile,)
from .models import UserInfo
admin.site.register(UserInfo,UserAdmin)