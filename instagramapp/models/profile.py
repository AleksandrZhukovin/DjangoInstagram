from django.db import models
from .abstract import Abstract
from django.contrib.auth.models import User


class Profile(Abstract):
    status = models.CharField(max_length=200, default=' ', null=True, blank=True)
    location = models.CharField(max_length=30, default=' ', null=True, blank=True)
    following = models.ManyToManyField(User, related_name='following')
    followers = models.ManyToManyField(User, related_name='followers')
