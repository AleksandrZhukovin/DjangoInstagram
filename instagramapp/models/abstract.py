from django.db import models
from django.contrib.auth.models import User


class Abstract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images')

    class Meta:
        abstract = True
