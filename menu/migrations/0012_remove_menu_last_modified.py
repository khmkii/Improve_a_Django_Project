# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 22:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0011_menu_last_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='last_modified',
        ),
    ]
