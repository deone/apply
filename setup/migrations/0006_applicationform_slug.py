# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 21:42
from __future__ import unicode_literals

from django.db import migrations
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0005_auto_20160402_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationform',
            name='slug',
            field=utils.AutoSlugField(db_index=False, editable=False, null=True, populate_from='name'),
        ),
    ]
