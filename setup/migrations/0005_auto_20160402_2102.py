# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0004_userapplication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userapplication',
            name='submit_date',
            field=models.DateTimeField(null=True, verbose_name='submit date'),
        ),
    ]
