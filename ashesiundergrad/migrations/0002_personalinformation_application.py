# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 22:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0011_auto_20160402_2153'),
        ('ashesiundergrad', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinformation',
            name='application',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='setup.Application'),
            preserve_default=False,
        ),
    ]
