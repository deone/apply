# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-08 11:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0013_auto_20160407_1131'),
        ('ashesiundergraduate', '0011_auto_20160408_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='passportdetails',
            name='user_application',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='setup.UserApplication'),
            preserve_default=False,
        ),
    ]
