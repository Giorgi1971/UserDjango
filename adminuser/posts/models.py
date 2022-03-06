from turtle import title
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime


user = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=124)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now())


class twitter(models.Model):
    follow = models.ForeignKey(User, on_delete=models.PROTECT, related_name='follow')
    followed = models.ForeignKey(User, on_delete=models.PROTECT, related_name='followed')