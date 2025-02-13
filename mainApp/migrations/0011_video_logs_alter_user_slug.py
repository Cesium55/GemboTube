# Generated by Django 5.0.2 on 2024-04-03 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0010_user_slug_alter_user_avatar_alter_video_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='logs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
