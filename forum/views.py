from django.shortcuts import render, HttpResponse, Http404, HttpResponseRedirect

# Create your views here.
from user.views import check_login
from .models import *
from django.views.decorators.csrf import csrf_exempt


@check_login
def index(request):
    items = Forum.objects.order_by("-created_time")
    return render(request, "forum/index.html", locals())


@check_login
def detail(request, title_id):
    try:
        item = Forum.objects.get(id=title_id)
    except:
        return Http404
    id = item.id
    title = item.title
    author = item.user
    content = item.content
    created_time = item.created_time
    updated_time = item.updated_time
    comments = item.comment_set.all()
    is_author = False
    if request.session['userName'] == item.user.username:
        is_author = True
    return render(request, 'forum/detail.html', locals())


@check_login
def update(request, title_id):
    try:
        item = Forum.objects.get(id=title_id)
    except:
        return Http404
    if request.method == 'GET':
        return render(request, 'forum/update.html', locals())
    elif request.method == 'POST':
        item.content = request.POST.get('content')
        # item.created_time=
        item.save()
        return HttpResponseRedirect(f'/forum/detail/{item.id}/')


@check_login
def add(request):
    if request.method == 'GET':
        return render(request, 'forum/add.html')
    elif request.method == 'POST':
        user = UserInfo.objects.get(username=request.session['userName'])
        data = request.POST
        title = data.get('title')
        content = data.get('content')
        Forum.objects.create(user=user, title=title, content=content)
        return HttpResponseRedirect('/forum/index')


@check_login
def delete(request, title_id):
    try:
        item = Forum.objects.get(id=title_id)
        item.delete()
        return HttpResponseRedirect('/forum/index')
    except:
        return Http404
