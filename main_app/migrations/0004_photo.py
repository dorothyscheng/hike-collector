# Generated by Django 3.2.3 on 2021-05-24 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_hike_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('hike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.hike')),
            ],
        ),
    ]
