# Generated by Django 4.2 on 2023-05-02 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(default='NAN', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='fname',
            field=models.CharField(default='NAN', max_length=100),
        ),
    ]
