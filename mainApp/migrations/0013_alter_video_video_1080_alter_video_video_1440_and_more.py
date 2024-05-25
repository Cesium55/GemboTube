# Generated by Django 5.0.2 on 2024-04-03 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0012_alter_video_logs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_1080',
            field=models.FileField(blank=True, null=True, upload_to='media/videos/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_1440',
            field=models.FileField(blank=True, null=True, upload_to='media/videos/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_2160',
            field=models.FileField(blank=True, null=True, upload_to='media/videos/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_240',
            field=models.FileField(blank=True, null=True, upload_to='media/videos/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_360',
            field=models.FileField(blank=True, null=True, upload_to='media/videos/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_480',
            field=models.FileField(blank=True, null=True, upload_to='media/videos/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_720',
            field=models.FileField(blank=True, null=True, upload_to='media/videos/%Y/%m/%d'),
        ),
    ]
