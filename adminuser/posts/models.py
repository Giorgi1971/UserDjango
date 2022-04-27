from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=124)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    like = models.ManyToManyField(User, related_name='users')

    def total_like(self):
        return self.like.count()

    def __str__(self) -> str:
        return self.title + ' | ' + str(self.author.pk) + ' | ' + str(self.pk)

    def get_absolute_url(self):
        return reverse("posts:post", kwargs={'pk': self.pk})

    # class Meta:
    #     ordering = ['-created']


class Comment(models.Model):
    text = models.CharField(max_length=256)
    mes_created = models.DateTimeField(default=timezone.now)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    @staticmethod
    def get_absolute_url():
        return reverse("posts:posts")


class Twitter(models.Model):
    follow = models.ForeignKey(User, on_delete=models.PROTECT, related_name='follow')
    followed = models.ForeignKey(User, on_delete=models.PROTECT, related_name='followed')

    class Meta:
        unique_together = [['follow', 'followed']]

    @staticmethod
    def get_absolute_url():
        return reverse('posts:posts')

    def __str__(self) -> str:
        return str(self.follow.pk)+' - '+str(self.followed.pk)

    # Must try to do this two line with view function - follow_user and unfollow get here.
    def following(self):
        Twitter(self.follow, self.followed).save()

    def unfollowing(self):
        Twitter(self.follow, self.followed).delete()
