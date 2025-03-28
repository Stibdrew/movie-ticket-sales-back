# Generated by Django 5.1.2 on 2025-03-15 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('venue', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('ar_model', models.FileField(upload_to='ar_models/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
