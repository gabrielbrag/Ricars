# Generated by Django 4.1 on 2023-05-06 15:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_vehicle_model_model_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='year',
            new_name='manufacture_year',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='model_year',
            field=models.IntegerField(default=2023, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(9999)]),
        ),
    ]
