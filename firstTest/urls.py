from django.urls import path
from .views import test,base
from forum.views import index
urlpatterns = [
     path('test',test),
     path('',base),
]