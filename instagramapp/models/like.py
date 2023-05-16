from django.db import models
from .abstract import Abstract
from .post import Post
from .comments import Comment


class Like(Abstract):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
