# Generated by Django 3.2.3 on 2021-05-28 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_auto_20210528_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='hike',
        ),
        migrations.AddField(
            model_name='hike',
            name='activities',
            field=models.ManyToManyField(to='main_app.Activity'),
        ),
    ]
