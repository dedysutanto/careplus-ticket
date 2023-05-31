# Generated by Django 4.1.9 on 2023-05-31 05:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketsused',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Ticket ID'),
        ),
    ]
