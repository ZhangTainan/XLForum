from django.urls import path
from .views import *

app_name = 'friends'
urlpatterns = [
    path('friends_list', friends_list, name='friends_list'),
    path('add_friend/<str:username>', add_friend, name='add_friend'),
    path('agree',agree,name="agree"),
    path('reject',reject,name='reject'),
]
