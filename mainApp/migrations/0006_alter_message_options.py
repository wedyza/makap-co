# Generated by Django 4.2 on 2023-05-06 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_alter_message_body_alter_message_getter_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['created']},
        ),
    ]
