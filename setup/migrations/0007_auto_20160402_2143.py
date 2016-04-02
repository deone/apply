# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 21:43
from __future__ import unicode_literals

from django.db import migrations
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0006_applicationform_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationform',
            name='slug',
            field=utils.AutoSlugField(db_index=False, null=True, populate_from='name'),
        ),
    ]
