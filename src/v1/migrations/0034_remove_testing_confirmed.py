# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-08-15 03:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0033_auto_20180815_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testing',
            name='confirmed',
        ),
    ]
