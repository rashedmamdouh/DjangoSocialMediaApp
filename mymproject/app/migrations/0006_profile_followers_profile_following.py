# Generated by Django 4.2 on 2023-05-09 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_likepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.IntegerField(default=0),
        ),
    ]
