# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 11:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0012_auto_20160404_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userapplication',
            name='submit_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='submit date'),
        ),
    ]