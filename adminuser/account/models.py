from sre_constants import SUCCESS
from django.db import models
from django.contrib.auth.models import User


class Author(User):
    image = models.ImageField(upload_to='profile')

    