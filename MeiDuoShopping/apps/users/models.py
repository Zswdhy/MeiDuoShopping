from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Users(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号码')

    class Meta:
        # 配置数据库表明，以及设置模型在admin站点显示的中文名
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
