# Generated by Django 3.2.3 on 2021-05-21 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_hike_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hike',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
