# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-08 11:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ashesiundergraduate', '0010_auto_20160407_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='passportdetails',
            options={'verbose_name_plural': 'Passport Details'},
        ),
        migrations.RemoveField(
            model_name='passportdetails',
            name='user_application',
        ),
    ]
