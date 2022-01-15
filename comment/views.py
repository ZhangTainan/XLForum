from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from user.views import check_login,UserInfo
from .models import Comment
from  forum.models import Forum
# Create your views here.
@check_login
def add(request,title_id):
    if request.method == 'GET':
        return render(request, 'comment/add.html',locals())
    elif request.method == 'POST':
        user = UserInfo.objects.get(username=request.session['userName'])
        forum=Forum.objects.get(id=title_id)
        data = request.POST
        content = data.get('content')
        Comment.objects.create(user=user,content=content,forum=forum)
        return HttpResponseRedirect(f'/forum/detail/{title_id}/')
