from django.db import models

# Create your models here.
# # 引入默认的用户模型类
# from django.contrib.auth.models import AbstractUser
#
#
# class UserProfile(AbstractUser):
#     # 昵称
#     # CharField的max_length是必填参数
#     # verbose_name 后台管理界面中显示的字段名
#     # 用户名
#     userName = models.CharField(verbose_name='用户名', max_length=20)
#     # 密码
#     password = models.CharField(verbose_name='密码', max_length=32)
#     nickName = models.CharField(verbose_name='昵称', default='', max_length=20)
#     # 生日
#     # blank=True 前端表单中的数据可以为空
#     birthday = models.DateTimeField(verbose_name='生日', null=True, blank=True)
#     # 性别
#     gender=models.CharField(verbose_name='性别',max_length=1)
#
#     # 住址
#     # address = models.CharField(max_length=50, verbose_name='地址', default='')
#
#     # 电话
#     # mobile = models.CharField(max_length=11, verbose_name='手机', default='')
#     # 邮箱
#     # email= models.EmailField(verbose_name="邮箱")
#
#     # 用户头像
#     # image = models.ImageField(upload_to='images/%Y/%m', default='image/default.png', verbose_name='头像')
#
#     class Meta:
#         db_table = 'Users'
#         # 后台管理界面中显示的表的信息
#         verbose_name = '用户信息'
#         # 复数
#         verbose_name_plural = '用户信息'
class UserInfo(models.Model):
    username=models.CharField(verbose_name='用户名',max_length=20,unique=True)
    password=models.CharField(verbose_name='密码',max_length=32)
    nickname=models.CharField(verbose_name='昵称',max_length=20,default='无名氏')
    gender=models.CharField(verbose_name='性别',max_length=1,choices=(('M','男'),('F','女')))
    age=models.IntegerField(verbose_name='年龄',default=18)
    # birthday=models.DateTimeField(verbose_name='出生日期',default='2021-01-01')
    email=models.EmailField(verbose_name='邮箱',max_length=30,unique=True)
    created_time=models.DateTimeField(verbose_name='注册时间',auto_now_add=True)
    class Meta:
        db_table='userinfo'
        verbose_name='普通用户',
        verbose_name_plural='普通用户'
    def __str__(self):
        return self.username
