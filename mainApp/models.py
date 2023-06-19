from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

nameEncounter = 0

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
    resume = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
                              blank=True)
    avatar = models.ImageField(upload_to='images/', default='../static/img/profile.png',
                               validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])],
                               blank=True)
    fullName = models.CharField(max_length=100, blank=False, default='ИмяПользователя')
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
    name = models.CharField(max_length=150, blank=False, default="Какой-то проект")
    image = models.ImageField(upload_to='images/', default='../static/img/photo404.jpg', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], blank=True)
    description = models.CharField(max_length=2000, blank=False, default="Описание какого-то проекта")
    link = models.CharField(max_length=250, blank=True, default="Какая-то ссылка")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

class Like(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey(userProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username + " лайкнул " + self.portfolio.name