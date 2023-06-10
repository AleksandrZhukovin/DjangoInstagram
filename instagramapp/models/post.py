from django.db import models
from .abstract import Abstract


class Post(Abstract):
    description = models.CharField(max_length=1000, default='')
    image = models.ImageField(upload_to='static/images/')
