# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0011_auto_20170321_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='calibrator',
            name='loss',
            field=models.DecimalField(decimal_places=8, default=1, max_digits=10),
        ),
    ]
