# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0008_climate_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='climatecontrol',
            name='value_max',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='climatecontrol',
            name='value_min',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8),
        ),
    ]
