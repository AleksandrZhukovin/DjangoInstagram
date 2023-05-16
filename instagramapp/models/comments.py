from django.db import models
from .post import Post
from .abstract import Abstract


class Comment(Abstract):
    body = models.CharField(max_length=1000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
