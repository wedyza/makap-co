from django.contrib import admin
from .models import Message, userProfile, Portfolio

# Register your models here.
admin.site.register(Message)
admin.site.register(userProfile)
admin.site.register(Portfolio)