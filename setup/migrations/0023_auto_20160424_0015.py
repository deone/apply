# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-24 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0022_auto_20160423_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='receive_fee',
        ),
        migrations.AddField(
            model_name='application',
            name='has_fee',
            field=models.BooleanField(default=False, verbose_name='has fee?'),
        ),
    ]
