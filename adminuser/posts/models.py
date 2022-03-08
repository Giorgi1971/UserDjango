from enum import unique
from turtle import title
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse, reverse_lazy


class Post(models.Model):
    title = models.CharField(max_length=124)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, default='Text for post...')
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    created = models.DateTimeField(default=datetime.now())

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('posts:user_page')


class Twitter(models.Model):
    follow = models.ForeignKey(User, on_delete=models.PROTECT, related_name='follow')
    followed = models.ForeignKey(User, on_delete=models.PROTECT, related_name='followed')

    class Meta:
        unique_together = [['follow', 'followed']]

    def get_absolute_url(self):
        return reverse('posts:posts')