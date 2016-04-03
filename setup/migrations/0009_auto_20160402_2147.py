# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 21:47
from __future__ import unicode_literals

from django.db import migrations
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0008_auto_20160402_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationform',
            name='slug',
            field=utils.AutoSlugField(blank=True, db_index=False, null=True, populate_from='form.name'),
        ),
    ]