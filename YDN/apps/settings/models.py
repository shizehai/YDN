
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
import register
class UserProfile(models.Model):
    # user = models.OneToOneField(User,blank=True,on_delete=models.CASCADE)
    user = models.CharField(max_length=50, verbose_name='用户名', default='')
    nick_name = models.CharField(max_length=50, blank=True,verbose_name='昵称', default='')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(max_length=6, blank=True,choices=(('male', '男'), ('female', '女')), default='female', verbose_name='性别')
    address = models.CharField(max_length=100, blank=True,default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    image = models.ImageField(max_length=100, blank=True,upload_to='image/%Y/%m', default='image?default.png', verbose_name='头像')

    class Meta:
        verbose_name = u'个人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return u'用户设置'

class sysProfile(models.Model):
    user = models.CharField(max_length=50, verbose_name='用户名', default='')
    nick_name = models.CharField(max_length=50, blank=True, verbose_name='昵称', default='')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(max_length=6, blank=True, choices=(('male', '男'), ('female', '女')), default='female',
                              verbose_name='性别')
    address = models.CharField(max_length=100, blank=True, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    image = models.ImageField(max_length=100, blank=True, upload_to='image/%Y/%m', default='image?default.png',
                              verbose_name='头像')

    class Meta:
        verbose_name = u'微信配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return u'微信配置'

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         profile = UserProfile()
#         profile.user = instance
#         profile.save()

@receiver(pre_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        last_user_name = User.objects.get(pk=instance.pk)
        one = UserProfile.objects.get(user=last_user_name)
        one.user = instance.username
        one.save()
    except:
        profile = UserProfile()
        profile.user = instance.username
        profile.save()
    ######
    try:
        last_user_name = User.objects.get(pk=instance.pk)
        one = sysProfile.objects.get(user=last_user_name)
        one.user = instance.username
        one.save()
    except:
        profile = sysProfile()
        profile.user = instance.username
        profile.save()
