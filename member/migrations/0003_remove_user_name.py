# Generated by Django 3.1.7 on 2023-06-17 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]
