# Generated by Django 5.1.7 on 2025-03-28 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_tickettype_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettype',
            name='name',
            field=models.CharField(default='Unnamed Ticket Type', max_length=255),
        ),
    ]
