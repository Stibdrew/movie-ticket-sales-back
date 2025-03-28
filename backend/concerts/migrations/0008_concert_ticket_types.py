# Generated by Django 5.1.7 on 2025-03-23 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concerts', '0007_alter_tickettype_price'),
        ('tickets', '0004_alter_tickettype_concert'),
    ]

    operations = [
        migrations.AddField(
            model_name='concert',
            name='ticket_types',
            field=models.ManyToManyField(related_name='concerts_related', to='tickets.tickettype'),
        ),
    ]
