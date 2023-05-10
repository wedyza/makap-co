from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

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



class userProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True)
    avatar = models.ImageField(upload_to='images/', default='../static/img/profile.png', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], blank=True)
    fullName = models.CharField(max_length=100, blank=False, default='похоже, тут ничего нет...')
    education = models.CharField(max_length=100, blank=False, default='похоже, тут ничего нет...')
    edu_base = models.CharField(max_length=100, blank=False, default='похоже, тут ничего нет...')
    contacts = models.CharField(max_length=250, blank=False, default='похоже, тут ничего нет...')
    level = models.CharField(max_length=100, blank=False, default='похоже, тут ничего нет...')
    chars = models.CharField(max_length=150, blank=False, default='похоже, тут ничего нет...')
    exp = models.CharField(max_length=200, blank=False, default='похоже, тут ничего нет...')


    def __str__(self):
        return self.user.username


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150, blank=False)
    image = models.ImageField(upload_to='images/', default='../static/img/photo404.jpg', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], blank=False)
    description = models.CharField(max_length=2000, blank=False)
    link = models.CharField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name