# Generated by Django 4.2 on 2023-05-09 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followers',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='following',
            name='following',
        ),
        migrations.AddField(
            model_name='followers',
            name='username',
            field=models.CharField(default='NAN', max_length=100),
        ),
        migrations.AddField(
            model_name='following',
            name='username',
            field=models.CharField(default='NAN', max_length=100),
        ),
    ]