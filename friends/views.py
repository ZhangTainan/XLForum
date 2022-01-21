from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import Http404

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
    friends = [{"username": fr.username_B, "remarkName": fr.remark_name_B} for fr in
               FriendRelationship.objects.filter(username_A=username)]
    friends += [{"username": fr.username_A, "remarkName": fr.remark_name_A} for fr in
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
        sender = UserInfo.objects.get(username=data.get("sender"))
        receiver = UserInfo.objects.get(username=data.get("receiver"))

        '''
            该条验证消息对接收者已经没有意义
            讲该条验证消息的是否同意设置为Y,修改验证消息为“xxx同意了你的好友请求”,
            互换接受者和发送者身份,这样发送者就会收到来自接收者的回馈消息
        '''
        val_mes = ValidationMessages.objects.get(id=inform_id)
        val_mes.isAgreed = 'Y'
        val_mes.content = f"{receiver.username}通过了你的好友验证！"
        val_mes.sender, val_mes.receiver = receiver, sender
        val_mes.save()

        # 若fr关系表中没有这对关系则在fr表中建立sender和receiver的朋友关系
        try:
            FriendRelationship.objects.get(username_A=sender.username, username_B=receiver.username)
        except:
            try:
                FriendRelationship.objects.get(username_A=receiver.username, username_B=sender.username)
            except:
                FriendRelationship.objects.create(username_A=sender.username, username_B=receiver.username,
                                                  remark_name_A=sender.username, remark_name_B=receiver.username)
        return HttpResponse(200)


@csrf_exempt
def reject(request):
    if request.method == "POST":
        data = request.POST
        inform_id = data.get('id')
        sender = UserInfo.objects.get(username=data.get("sender"))
        receiver = UserInfo.objects.get(username=data.get("receiver"))

        '''
            该条验证消息对接收者已经没有意义
            讲该条验证消息的是否同意设置为N,修改验证消息为“xxx婉拒了你的好友请求”,
            互换接受者和发送者身份,这样发送者就会收到来自接收者的回馈消息
        '''
        val_mes = ValidationMessages.objects.get(id=inform_id)
        val_mes.isAgreed = 'N'
        val_mes.content = f"{receiver.username}婉拒了你的好友请求！"
        val_mes.sender, val_mes.receiver = receiver, sender
        val_mes.save()
        print('123')

        return HttpResponse(200)


@csrf_exempt
def del_val_mes(request):
    if request.method == "POST":
        val_mes_id = request.POST.get('id')
        ValidationMessages.objects.get(id=val_mes_id).delete()
        # 返回一个响应防止报错
        return HttpResponse(200)


@check_login
def delete_friend(request, username):
    # 获取session中的当前用户名和参数用户名
    # 在数据库中删除这对好友关系
    username_myself = request.session.get('userName')
    print(username)
    try:
        fr = FriendRelationship.objects.get(username_A=username_myself, username_B=username)
        fr.delete()
        return HttpResponseRedirect('/friends/friends_list')
    except:
        try:
            fr = FriendRelationship.objects.get(username_B=username_myself, username_A=username)
            fr.delete()
            return HttpResponseRedirect('/friends/friends_list')

        except:
            return render(request, '404.html')
