# Generated by Django 3.1.7 on 2023-06-17 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_remove_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='noname', max_length=30),
        ),
    ]
