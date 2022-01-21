from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import json
# Create your views here.
from .models import UserInfo
from hashlib import md5
from friends.models import *
from django.db.models import F, Q


def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        if {'username': username} in UserInfo.objects.values('username'):
            return HttpResponse('用户名已存在！')
        password = request.POST.get('password')
        if password:
            m_password = md5()
            m_password.update(password.encode())
            password = m_password.hexdigest()
        nickname = request.POST.get('nickname')
        gender = request.POST.get('gender')
        # print(gender)

        age = request.POST.get('age')
        email = request.POST.get('email')
        try:
            UserInfo.objects.create(username=username, password=password,
                                    nickname=nickname, gender=gender,
                                    age=age, email=email)
        except:
            return HttpResponse('用户名或邮箱已被注册')
        return render(request, 'user/login.html', locals())


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = UserInfo.objects.get(username=username)
        except Exception as e:
            return HttpResponse('用户名或密码错误')
        password = request.POST.get('password')
        m_password = md5()
        m_password.update(password.encode())
        password = m_password.hexdigest()
        if password == user.password:
            request.session['userName'] = username
            request.session['userID'] = user.id
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('用户名或密码错误')


def check_login(func):
    def wrapper(request, *args, **kwargs):
        if 'userName' in request.session and 'userID' in request.session:

            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/user/login')

    return wrapper


def logout(request):
    if request.session.get('userName'):
        del request.session['userName']
    if request.session.get('userID'):
        del request.session['userID']
    return HttpResponseRedirect('/')


@check_login
def index(request):
    username = request.session['userName']
    user = UserInfo.objects.get(username=username)
    if user.gender == 'M':
        user.gender = '男'
    else:
        user.gender = '女'
    return render(request, 'user/index.html', locals())


@check_login
def modify(request):
    user = UserInfo.objects.get(username=request.session['userName'])
    if request.method == 'GET':
        return render(request, 'user/modify.html', locals())
    elif request.method == 'POST':
        data = request.POST
        user.age = data.get('age')
        user.nickname = data.get('nickname')
        user.gender = data.get('gender')
        user.save()
        return HttpResponseRedirect('/user/index')


@check_login
def changePassword(request):
    # 后续改成用userID索引用户，因为id有索引
    user = UserInfo.objects.get(username=request.session['userName'])
    if request.method == 'GET':
        return render(request, 'user/changePassword.html', locals())
    elif request.method == 'POST':
        password = request.POST.get('password')
        m_password = md5()
        m_password.update(password.encode())
        password = m_password.hexdigest()
        user.password = password
        user.save()
        return HttpResponseRedirect('/user/index')


@check_login
def information(request, username):
    username_myself = request.session['userName']
    '''
        判断两个用户是不是在关系表里,在则是好友关系
    '''
    isFriend = (bool(FriendRelationship.objects.filter(Q(username_A=username) & Q(username_B=username_myself)))
                or bool(FriendRelationship.objects.filter(Q(username_B=username) & Q(username_A=username_myself))))
    # isFriend=False
    if username_myself == username:
        # 是用户自己返回主页
        return HttpResponseRedirect('/user/index')
    # 把用户信息查出来返回前端
    user = UserInfo.objects.get(username=username)
    if user.gender == 'M':
        user.gender = '男'
    else:
        user.gender = '女'
    return render(request, 'user/information.html', locals())


@check_login
def notifications(request):
    return render(request, 'user/notifications.html')


@check_login
def val_mes(request):
    username = request.session['userName']
    user = UserInfo.objects.get(username=username)
    informs = ValidationMessages.objects.filter(receiver=user)
    return render(request, 'user/val_mes.html', locals())


# 增加搜索用户
@check_login
def search_user(request):
    print(request.GET)
    print(type(request.GET))
    username=request.GET.get('username')
    user=UserInfo.objects.get(username=username)
    data={
        "username":username,
        "nickname":user.nickname,
        "gender":'男' if user.gender=='M' else '女' ,
        "age":user.age,
    }
    print(json.dumps(data,ensure_ascii=False))
    return HttpResponse(json.dumps(data,ensure_ascii=False))
