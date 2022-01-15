from django.shortcuts import render
from user.views import check_login

# Create your views here.
@check_login
def tree(request):
    return render(request,'xlTree/xlTree.html')