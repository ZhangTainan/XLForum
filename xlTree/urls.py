from django.urls import path
from .views import *
app_name='xlTree'
urlpatterns = [
    path('',tree,name='index'),
]