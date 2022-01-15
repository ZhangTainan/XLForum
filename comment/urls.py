from django.urls import path
from .views import *

app_name = 'comment'
urlpatterns = [

    path('add/<int:title_id>', add, name='add'),

]
