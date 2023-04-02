from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    members = models.ManyToManyField(User, related_name='members')
