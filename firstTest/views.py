from django.shortcuts import render, HttpResponse

from user.views import check_login
# Create your views here.
@check_login
def test(request):
    # render(request,"")
    # return render(request, 'firstTest/test.html')
    return HttpResponse(200)


def base(request):
    logged=False
    if 'userName' in request.session and 'userID' in request.session:
        username=request.session['userName']
        logged=True
    return render(request,'base.html',locals())

