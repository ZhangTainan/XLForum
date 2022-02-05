import json

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import Http404

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from user.views import check_login
from user.models import UserInfo
from .models import *
from django.db.models import Q, F


@check_login
def friends_list(request):
    username = request.session['userName']

    # friends=FriendRelationship.objects.filter(Q(FriendRelationship.username_A=='username'
    #                                             | Q(FriendRelationship.username_B)))
    friends = [{"username": fr.username_B, "remarkName": fr.remark_name_B} for fr in
               FriendRelationship.objects.filter(username_A=username)]
    friends += [{"username": fr.username_A, "remarkName": fr.remark_name_A} for fr in
                FriendRelationship.objects.filter(username_B=username)]

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


@check_login
def dialogues(request):
    '''
    查询出与该用户有过聊天的用户,去重后渲染出对话框
    '''
    user_id = request.session.get('userID')
    user = UserInfo.objects.get(id=user_id)
    receivers = list(map(lambda x: x.receiver, Dialogue.objects.filter(sender=user)))
    senders = list(map(lambda x: x.sender, Dialogue.objects.filter(receiver=user)))
    related_users = list(set(receivers + senders))

    dialogues_list = []  # 定义一个空列表存需要渲染的对话框数据
    for related_user in related_users:
        # 根据相关用户查询出与该用户最新一条消息记录和发送时间
        dia = Dialogue.objects.filter(
            Q(sender=related_user) & Q(receiver=user) | Q(sender=user) & Q(receiver=related_user)).order_by(
            '-send_time')[0]
        dialogues_list.append({
            "user": related_user,
            "message": dia.message,
            "send_time": dia.send_time,

        })

    return render(request, 'friends/dialogues.html', context={'dialogues': dialogues_list})


@check_login
def detail_dialogues(request):
    '''
    查询出这两个用户之间的所有对话
    按时间排序渲染在对话框中
    '''
    try:
        user = UserInfo.objects.get(username=request.session.get('userName'))
        related_user = UserInfo.objects.get(username=request.GET.get('username'))

        dialogue_objects = Dialogue.objects.filter(
            Q(sender=related_user) & Q(receiver=user) | Q(sender=user) & Q(receiver=related_user)).order_by(
            'send_time')
        dialogues_list = []
        for dialogue_object in dialogue_objects:
            dialogues_list.append({
                "username": dialogue_object.sender.username,
                "message": dialogue_object.message,
                "send_time": str(dialogue_object.send_time),
            })
        print(json.dumps(dialogues_list))
        return HttpResponse(json.dumps(dialogues_list))
    except:
        return render(request, '404.html')


# @check_login
@csrf_exempt
def send_message(request):
    '''
    接受ajax请求,存储发送过来的ajax对话数据
    '''
    sender_name = request.POST.get("send_name")
    receiver_name = request.POST.get("receiver_name")
    sender = UserInfo.objects.get(username=sender_name)
    receiver = UserInfo.objects.get(username=receiver_name)
    message = request.POST.get("message")
    Dialogue.objects.create(sender=sender, receiver=receiver, message=message)
    return HttpResponse(200)


# TODO:解决csrf_exempt装饰的视图函数的跨站请求伪造问题

@csrf_exempt
def set_remark_name(request):
    data = request.POST
    user = data.get('username')
    friend = data.get('friendUsername')
    remarkName = data.get('remarkName')
    print(user,friend,remarkName)
    try:
        fr = FriendRelationship.objects.get(username_A=user, username_B=friend)
        fr.remark_name_B = remarkName
        fr.save()
        return HttpResponse("success")
    except:
        try:
            fr = FriendRelationship.objects.get(username_A=friend, username_B=user)
            fr.remark_name_A = remarkName
            fr.save()
            return HttpResponse("success")
        except:
            return HttpResponse(404)
