# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-13 00:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sysProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='', max_length=50, verbose_name='用户名')),
                ('nick_name', models.CharField(blank=True, default='', max_length=50, verbose_name='昵称')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('gender', models.CharField(blank=True, choices=[('male', '男'), ('female', '女')], default='female', max_length=6, verbose_name='性别')),
                ('address', models.CharField(blank=True, default='', max_length=100, verbose_name='地址')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号')),
                ('image', models.ImageField(blank=True, default='image?default.png', upload_to='image/%Y/%m', verbose_name='头像')),
            ],
            options={
                'verbose_name': '微信配置',
                'verbose_name_plural': '微信配置',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='', max_length=50, verbose_name='用户名')),
                ('nick_name', models.CharField(blank=True, default='', max_length=50, verbose_name='昵称')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('gender', models.CharField(blank=True, choices=[('male', '男'), ('female', '女')], default='female', max_length=6, verbose_name='性别')),
                ('address', models.CharField(blank=True, default='', max_length=100, verbose_name='地址')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号')),
                ('image', models.ImageField(blank=True, default='image?default.png', upload_to='image/%Y/%m', verbose_name='头像')),
            ],
            options={
                'verbose_name': '个人信息',
                'verbose_name_plural': '个人信息',
            },
        ),
    ]
