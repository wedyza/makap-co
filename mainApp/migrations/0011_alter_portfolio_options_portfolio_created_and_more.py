# Generated by Django 4.2 on 2023-05-10 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0010_portfolio_alter_userprofile_avatar_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='portfolio',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='portfolio',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portfolio',
            name='name',
            field=models.CharField(default=2, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portfolio',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]