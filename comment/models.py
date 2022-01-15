from django.db import models
from user.models import UserInfo
from forum.models import Forum

# Create your models here.
class Comment(models.Model):
    content = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField('评论时间', auto_now_add=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    forum=models.ForeignKey(Forum,on_delete=models.CASCADE)
    class Meta:
        db_table='comment'
        verbose_name = '评论'
        verbose_name_plural = '评论'