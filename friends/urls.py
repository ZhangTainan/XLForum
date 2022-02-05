from django.urls import path

from forum.views import delete
from .views import *

app_name = 'friends'
urlpatterns = [
    path('friends_list', friends_list, name='friends_list'),
    path('add_friend/<str:username>', add_friend, name='add_friend'),
    path('agree', agree, name="agree"),
    path('reject', reject, name='reject'),
    path('del_val_mes', del_val_mes, name="del_val_mes"),
    path('delete_friend/<str:username>', delete_friend, name='delete_friend'),
    path('dialogues', dialogues, name='dialogues'),
    path('detail_dialogues', detail_dialogues, name='detail_dialogues'),
    path('send_message', send_message, name='send_message'),
    path('set_remark_name', set_remark_name, name='set_remark_name'),
]
