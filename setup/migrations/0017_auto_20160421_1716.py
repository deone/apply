# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-21 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0016_auto_20160415_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='short_name',
        ),
        migrations.AddField(
            model_name='organization',
            name='slug',
            field=models.SlugField(default='a', verbose_name='slug'),
            preserve_default=False,
        ),
    ]
