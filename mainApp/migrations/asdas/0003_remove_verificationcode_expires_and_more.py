# Generated by Django 5.0.2 on 2024-02-13 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_alter_user_avatar_verificationcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verificationcode',
            name='expires',
        ),
        migrations.AddField(
            model_name='verificationcode',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='verificationcode',
            name='lastCreated',
            field=models.DateField(auto_now=True),
        ),
    ]
