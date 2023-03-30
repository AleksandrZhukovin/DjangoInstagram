from django.contrib.auth.models import User
from django.db import models
from .post import Post


class Comment(models.Model):
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)