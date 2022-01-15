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
    path('inform',inform,name='inform'),
]