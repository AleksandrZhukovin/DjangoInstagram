from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    location = models.CharField(max_length=30, default=' ')
    avatar = models.ImageField(upload_to='static/avatars')
