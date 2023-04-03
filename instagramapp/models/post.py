from django.db import models
from .abstract import Abstract
from .profile import Profile


class Post(Abstract):
    description = models.CharField(max_length=1000, default=' ')
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
