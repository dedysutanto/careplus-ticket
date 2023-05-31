# Generated by Django 4.1.9 on 2023-05-31 05:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Ticket Name')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Ticket ID')),
                ('phonenumber', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '0899999999'. Up to 16 digits allowed.", regex='^\\0?1?\\d{9,16}$')], verbose_name='WA Number')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('amount', models.IntegerField(default=1, verbose_name='Ticket Amount')),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ticket Sell',
                'verbose_name_plural': 'Tickets Sell',
                'db_table': 'tickets',
            },
        ),
        migrations.CreateModel(
            name='TicketsClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Class Name')),
                ('price', models.IntegerField(blank=True, default=0)),
            ],
            options={
                'verbose_name': 'Ticket Class',
                'verbose_name_plural': 'Tickets Class',
                'db_table': 'tickets_class',
            },
        ),
        migrations.CreateModel(
            name='TicketsUsed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Ticket ID')),
                ('ticket_number', models.IntegerField(default=0, verbose_name='Ticket Number')),
                ('time_used', models.DateTimeField(auto_now_add=True)),
                ('is_used', models.BooleanField(default=False, editable=False, verbose_name='Is Used')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.tickets')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
                'db_table': 'tickets_used',
            },
        ),
        migrations.AddField(
            model_name='tickets',
            name='ticket_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tickets.ticketsclass'),
        ),
    ]
