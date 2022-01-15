from django.urls import path
# from django.contrib import
from .views import *

app_name='cs'
urlpatterns = [
    path('index',index,name='index'),
    path('classSchedule', classSchedule,name='classSchedule'),
    path('javaDocumentation', javaDocumentation,name='javaDocumentation'),
    path('javaExam',javaExam,name='javaExam'),
]
