# Generated by Django 4.2 on 2023-05-08 08:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0007_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to='images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='resume',
            field=models.FileField(upload_to='files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
