from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.CharField(max_length=200, default='', null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, default='', blank=True)
    website = models.CharField(max_length=250, null=True, default='', blank=True)
    image = models.ImageField(upload_to='media/profs/', default='media/profs/default.png')
