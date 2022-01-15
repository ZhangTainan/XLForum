from django.db import models

# Create your models here.
from user.models import UserInfo


class FriendRelationship(models.Model):
    '''
        关系表，只记录两个用户的用户名和成为朋友关系的时间
        及互相的备注名
    '''
    username_A=models.CharField(verbose_name='用户A',max_length=20)
    username_B=models.CharField(verbose_name='用户B',max_length=20)
    remark_name_A=models.CharField(verbose_name='A的备注',max_length=20,null=True)
    remark_name_B=models.CharField(verbose_name='B的备注',max_length=20,null=True)
    added_time=models.DateTimeField(verbose_name='添加时间',auto_now_add=True)
    class Meta:
        db_table='FR'# FriendRelationship
        verbose_name = '好友关系'
        verbose_name_plural = '好友关系'
        ordering = ["added_time"]

# class Friend(models.Model):
#
#     user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
#     username = models.CharField(verbose_name='用户名', max_length=20)
#     remarkName = models.CharField(verbose_name='昵称', max_length=20, null=True)
#     added_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
#
#     class Meta:
#         db_table = 'friends'
#         verbose_name = '好友'
#         verbose_name_plural = '好友'
#         ordering = ['user', "added_time"]


class ValidationMessages(models.Model):
    '''
        获取发送好友请求的人，接受的信息的人，将验证信息渲染再接收者的页面
    '''
    sender = models.ForeignKey(UserInfo, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserInfo, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='消息')
    send_time = models.DateTimeField(verbose_name='发送时间',auto_now_add=True)
    isAgreed = models.BooleanField(verbose_name='是否同意', default=False, choices=((False, '不同意'), (True, '同意')))

    # 根据是否同意确定是否成为好友关系
    class Meta:
        db_table = 'val_mes'


class Dialogue(models.Model):
    user=models.ForeignKey(UserInfo,related_name='dialogue_user',on_delete=models.CASCADE)
    friend=models.ForeignKey(UserInfo,related_name='dialogue_friend',on_delete=models.CASCADE)
    message=models.TextField(verbose_name='消息')
    send_time=models.DateTimeField(verbose_name='发送时间',auto_now_add=True)
    '''
        根据user和friend按日期查询出结果并渲染
    '''
    '''
        当用户点击某个好友时，将与该好友的对话进行渲染
        两个好友的全部对话按按时间顺序渲染。
    '''
    class Meta:
        db_table='messages'
