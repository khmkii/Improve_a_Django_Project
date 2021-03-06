# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 19:23
from __future__ import unicode_literals
from datetime import date

from django.db import migrations, models


def datetime_to_date(apps, schema_editor):
    Menu = apps.get_model('menu', 'menu')
    for menu in Menu.objects.all():
        menu.c_date = menu.created_date.date()
        menu.save()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20170131_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='c_date',
            field=models.DateField(default=date.today),
            preserve_default=True,
        ),
        migrations.RunPython(datetime_to_date),
        migrations.RemoveField(
            model_name='menu',
            name='created_date'
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='c_date',
            new_name='created_date'
        ),
    ]
