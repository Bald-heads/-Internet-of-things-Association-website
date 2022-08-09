# Generated by Django 3.2.12 on 2022-05-17 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_name', models.CharField(max_length=8, verbose_name='管理员姓名')),
                ('admin_number', models.CharField(max_length=12, verbose_name='学号')),
                ('admin_password', models.CharField(max_length=32, verbose_name='管理员密码')),
            ],
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_index=True, max_length=8, verbose_name='姓名')),
                ('student_number', models.CharField(max_length=32, verbose_name='学号')),
                ('student_qq', models.CharField(max_length=12, verbose_name='QQ号')),
                ('mobile_phone', models.CharField(max_length=32, verbose_name='手机号')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
            ],
        ),
    ]