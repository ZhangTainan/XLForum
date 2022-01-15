from django.contrib import admin

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content','user','forum','created_time']
    list_filter = ['user','created_time']
    list_display_links = ['content']

#
# admin.site.register(UserProfile,)
from .models import Comment
admin.site.register(Comment,CommentAdmin)