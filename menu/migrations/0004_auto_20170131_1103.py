# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20170131_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
