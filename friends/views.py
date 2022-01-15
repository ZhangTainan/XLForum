from django.shortcuts import render, HttpResponseRedirect, HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from user.views import check_login
from user.models import UserInfo
from .models import *
from django.db.models import Q


@check_login
def friends_list(request):
    username = request.session['userName']

    # friends=FriendRelationship.objects.filter(Q(FriendRelationship.username_A=='username'
    #                                             | Q(FriendRelationship.username_B)))
    friends = [{"username": ship.username_B, "remarkName": ship.remark_name_B} for ship in
               FriendRelationship.objects.filter(username_A=username)]
    friends += [{"username": ship.username_A, "remarkName": ship.remark_name_A} for ship in
                FriendRelationship.objects.filter(username_B=username)]
    print(friends)
    return render(request, 'friends/friends_list.html', locals())


@check_login
def add_friend(request, username):
    sender = UserInfo.objects.get(username=request.session['userName'])
    receiver = UserInfo.objects.get(username=username)
    if request.method == 'GET':
        return render(request, 'friends/validationMessage.html', locals())
    elif request.method == 'POST':
        # 添加好友时在两个用户之间建立一个验证消息会话
        # 即在数据库中新建一条会话记录
        content = request.POST.get('content', f'{sender}请求添加你为好友！')
        ValidationMessages.objects.create(sender=sender, receiver=receiver, content=content)
        print(content)
        return HttpResponseRedirect('/friends/friends_list')


@csrf_exempt
def agree(request):
    if request.method == "POST":
        data = request.POST
        inform_id = data.get('id')
        sender = data.get("sender")
        receiver = data.get("receiver")

        # 删除这条验证消息
        ValidationMessages.objects.get(id=inform_id).delete()

        # 若fr关系表中没有这对关系则在fr表中建立sender和receiver的朋友关系
        try:
            FriendRelationship.objects.get(username_A=sender, username_B=receiver)
        except:
            try:
                FriendRelationship.objects.get(username_A=receiver, username_B=sender)
            except:
                FriendRelationship.objects.create(username_A=sender, username_B=receiver,
                                                  remark_name_A=sender, remark_name_B=receiver)
        return HttpResponse(200)


@csrf_exempt
def reject(request):
    if request.method == "POST":
        data = request.POST
        inform_id = data.get('id')
        sender = data.get("sender")
        receiver = data.get("receiver")

        # 把该条验证消息删除，并回馈发送者”拒绝“的信息
        ValidationMessages.objects.get(id=inform_id).delete()
        # TODO:添加回馈拒绝信息
        return HttpResponse(200)


@check_login
def delete_friend(request):
    pass
