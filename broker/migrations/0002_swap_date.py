# Generated by Django 5.1.3 on 2025-02-12 09:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='swap',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
