from django.contrib import admin
from .models import Message, userProfile, Portfolio, Like

# Register your models here.
admin.site.register(Message)
admin.site.register(userProfile)
admin.site.register(Portfolio)
admin.site.register(Like)