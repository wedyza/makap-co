# Generated by Django 4.2 on 2023-06-19 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0007_like_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='description',
            field=models.CharField(default='Описание какого-то проекта', max_length=2000),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='link',
            field=models.CharField(blank=True, default='Какая-то ссылка', max_length=250),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='name',
            field=models.CharField(default='Какой-то проект', max_length=150),
        ),
    ]
