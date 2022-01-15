from django.db import models
from user.models import UserInfo
# Create your models here.
'''
    发布者，主题，内容，时间，修改时间，删除,注册后台
'''
class Forum(models.Model):

    title=models.CharField(verbose_name='主题',max_length=100)
    content=models.TextField(verbose_name='内容')
    created_time=models.DateTimeField(verbose_name='发布时间',auto_now_add=True)
    updated_time=models.DateTimeField(verbose_name='更新时间',auto_now=True)
    user=models.ForeignKey(UserInfo,on_delete=models.CASCADE)

    class Meta:
        db_table='forum'
        verbose_name='论坛话题'
        verbose_name_plural='论坛话题'
        ordering=["-created_time"]
    def __str__(self):
        return self.title
