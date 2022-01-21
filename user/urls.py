from django.urls import path
from .views import *
app_name='user'
urlpatterns = [
    path('register',register,name='register'),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('index',index,name='index'),
    path('modifyUserInfo',modify,name='modify'),
    path('changePassword',changePassword,name='changePassword'),
    path('information/<str:username>/',information,name='information'),
    path('notifications',notifications,name='notifications'),
    path('val_mes',val_mes,name='val_mes'),
    path('search_user',search_user,name='search_user'),
]
