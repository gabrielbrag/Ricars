# Generated by Django 4.1.6 on 2023-04-26 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0002_alter_vehicle_vehicle_variant_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle_model',
            name='model_type',
            field=models.CharField(choices=[('M', 'Motorcycle'), ('C', 'Car'), ('T', 'Truck')], default='C', max_length=1),
            preserve_default=False,
        ),
    ]
