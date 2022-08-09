from django.db import models


# Create your models here.
# 成员类
class StudentInfo(models.Model):
    username = models.CharField(verbose_name="姓名", max_length=8, db_index=True)
    student_number = models.CharField(verbose_name='学号', max_length=32)
    student_qq = models.CharField(verbose_name="QQ号", max_length=12)
    mobile_phone = models.CharField(verbose_name="手机号", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )

    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class Admin(models.Model):
    admin_name = models.CharField(verbose_name="管理员姓名", max_length=8)
    admin_number = models.CharField(verbose_name="学号", max_length=12)
    admin_password = models.CharField(verbose_name="管理员密码", max_length=32)
