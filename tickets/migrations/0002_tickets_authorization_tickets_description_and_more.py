# Generated by Django 4.1.9 on 2023-06-01 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='authorization',
            field=models.BooleanField(default=False, verbose_name='Authorization'),
        ),
        migrations.AddField(
            model_name='tickets',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='tickets',
            name='faith_promise',
            field=models.IntegerField(default=0, verbose_name='Janji Iman'),
        ),
        migrations.AddField(
            model_name='ticketsclass',
            name='seats',
            field=models.IntegerField(default=0, verbose_name='Number of Seats'),
        ),
    ]
