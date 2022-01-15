from django.urls import path
from .views import *
app_name='loveBar'
urlpatterns = [
    path('',bar,name='index'),
]