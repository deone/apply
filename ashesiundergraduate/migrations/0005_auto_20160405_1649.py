# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-05 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ashesiundergraduate', '0004_auto_20160405_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinformation',
            name='photo_height',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='photo_width',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
    ]