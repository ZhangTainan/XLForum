from django.urls import path

from forum.views import delete
from .views import *

app_name = 'friends'
urlpatterns = [
    path('friends_list', friends_list, name='friends_list'),
    path('add_friend/<str:username>', add_friend, name='add_friend'),
    path('agree',agree,name="agree"),
    path('reject',reject,name='reject'),
    path('del_val_mes',del_val_mes,name="del_val_mes"),
    path('delete_friend/<str:username>', delete_friend, name='delete_friend'),
]
