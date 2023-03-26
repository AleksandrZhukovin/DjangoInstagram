from django.db import models
from abstract import Abstract


class Post(Abstract):
    description = models.CharField(max_length=1000)
