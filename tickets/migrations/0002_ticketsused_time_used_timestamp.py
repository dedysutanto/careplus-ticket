# Generated by Django 4.1.9 on 2023-06-03 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketsused',
            name='time_used_timestamp',
            field=models.IntegerField(default=0),
        ),
    ]