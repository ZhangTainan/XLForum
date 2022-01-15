from django.shortcuts import render
from user.views import check_login

# Create your views here.
@check_login
def index(request):
    return render(request,'cs/index.html')
@check_login
def classSchedule(request):
    return render(request,'cs/table.html')
@check_login
def javaDocumentation(request):
    return render(request,'cs/javaDocumentation.html')
@check_login
def javaExam(request):
    return render(request,'cs/javaExam.html')