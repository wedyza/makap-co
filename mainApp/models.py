from django.db import models
from django.contrib.auth.models import User
class Message(models.Model):
    # sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    # getter = models.ForeignKey(User, related_name='getter', on_delete=models.CASCADE)
    # body = models.TextField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=50)
    getter = models.CharField(max_length=50)
    body = models.CharField(max_length=200)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.body
