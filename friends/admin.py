from django.contrib import admin

# Register your models here.
class FriendAdmin(admin.ModelAdmin):
    # list_display = ['user','username','remarkName','added_time']
    # list_filter = ['user','added_time']
    # list_display_links = ['user','username']
    pass

from .models import FriendRelationship
admin.site.register(FriendRelationship,FriendAdmin)