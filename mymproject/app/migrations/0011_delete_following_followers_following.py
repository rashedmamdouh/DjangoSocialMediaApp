# Generated by Django 4.2 on 2023-05-10 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_followers_follower_following_following'),
    ]

    operations = [
        migrations.DeleteModel(
            name='following',
        ),
        migrations.AddField(
            model_name='followers',
            name='following',
            field=models.CharField(default='NAN', max_length=100),
        ),
    ]
