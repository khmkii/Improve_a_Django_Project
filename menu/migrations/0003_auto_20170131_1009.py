# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredients', to='menu.Ingredient'),
        ),
    ]
