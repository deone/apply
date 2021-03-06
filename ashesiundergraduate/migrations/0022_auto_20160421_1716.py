# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-21 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ashesiundergraduate', '0021_auto_20160414_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinformation',
            name='alternative_phone_number',
            field=models.CharField(help_text='Phone numbers must be prefixed with country code e.g. +233xxxxxxxxx', max_length=15, null=True, verbose_name='alternative phone number'),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='primary_phone_number',
            field=models.CharField(help_text='Phone numbers must be prefixed with country code e.g. +233xxxxxxxxx', max_length=15, verbose_name='primary phone number'),
        ),
    ]
