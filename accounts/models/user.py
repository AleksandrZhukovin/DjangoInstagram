from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    status = models.CharField(max_length=200, default='', null=True, blank=True)
    image = models.ImageField(upload_to='instagram/static/images/', default='instagram/static/images/default.png')
