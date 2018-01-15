from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

def register_userinfo(profileModel):
    @receiver(post_save, sender=User)
    def save_user_profile(sender,instance, **kwargs):
        try:
            one = profileModel.objects.get(user=User.username)
            one.user = instance.username
            one.save()
        except:
            profile = profileModel()
            profile.user = instance.username
            profile.save()

    @receiver(pre_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        try:
            last_user_name = User.objects.get(pk=instance.pk)
            one = profileModel.objects.get(user=last_user_name)
            one.user = instance.username
            one.save()
        except:
            profile = profileModel()
            profile.user = instance.username
            profile.save()