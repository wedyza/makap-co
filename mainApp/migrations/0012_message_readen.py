# Generated by Django 4.2 on 2023-05-21 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0011_alter_portfolio_options_portfolio_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='readen',
            field=models.BooleanField(default='false'),
            preserve_default=False,
        ),
    ]
