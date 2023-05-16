from django.db import models
from .user import User


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following')
    followers = models.ManyToManyField(User, related_name='followers')
