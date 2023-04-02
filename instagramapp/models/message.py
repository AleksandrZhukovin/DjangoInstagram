from django.contrib.auth.models import User
from django.db import models
from .chat import Chat


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=10000)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
