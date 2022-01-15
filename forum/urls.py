from django.urls import path
from .views import *

app_name = 'forum'
urlpatterns = [
    path('index', index, name='index'),
    path('add', add, name='add'),
    path('detail/<int:title_id>/', detail,name='detail'),
    path('update/<int:title_id>/', update,name='update'),
    path('delete/<int:title_id>/', delete,name='delete'),
]
