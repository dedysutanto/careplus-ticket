# Generated by Django 4.1.9 on 2023-06-01 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_ticketsclasschild_tickets_ticket_class_child'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketsclasschild',
            name='parent_class',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='tickets.ticketsclass'),
        ),
    ]
