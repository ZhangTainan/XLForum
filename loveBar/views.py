from django.shortcuts import render
from user.views import check_login
# Create your views here.
@check_login
def bar(request):
    return render(request,'loveBar/loveBar.html')