# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-10 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_remove_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.CharField(default='', max_length=50, verbose_name='用户名'),
        ),
    ]