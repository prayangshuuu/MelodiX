# Generated by Django 5.1.3 on 2024-11-20 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('melodixapp', '0006_store_remove_artist_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='label',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='melodixapp.label'),
        ),
    ]
