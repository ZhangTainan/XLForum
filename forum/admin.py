from django.contrib import admin


# Register your models here.
class ForumAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'user', 'created_time']
    list_filter = ['title', 'created_time']
    list_display_links = ['title']


#
# admin.site.register(UserProfile,)
from .models import Forum

admin.site.register(Forum, ForumAdmin)
