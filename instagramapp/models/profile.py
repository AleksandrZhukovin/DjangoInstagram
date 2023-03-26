from django.db import models
from django.contrib.auth.models import User
from abstract import Abstract


class Profile(Abstract):
    status = models.CharField(max_length=200)
    location = models.CharField(max_length=30, default=' ')
