# Generated by Django 5.1.7 on 2025-03-23 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_alter_tickettype_concert'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickettype',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tickettype',
            name='category',
            field=models.CharField(blank=True, choices=[('VIP', 'VIP (200 pax)'), ('LB', 'Lower Box (500 pax)'), ('UB', 'Upper Box (800 pax)'), ('GA', 'General Admission (1500 pax)')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='tickettype',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='tickettype',
            name='remaining_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tickettype',
            name='total_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
