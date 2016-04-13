# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-12 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ashesiundergraduate', '0017_auto_20160412_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinformation',
            name='alternative_phone_number',
            field=models.CharField(help_text='Enter phone number in the format +233xxxxxxxxx', max_length=15, null=True, verbose_name='alternative phone number'),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='primary_phone_number',
            field=models.CharField(default=1, help_text='Enter phone number in the format +233xxxxxxxxx', max_length=15, verbose_name='primary phone number'),
            preserve_default=False,
        ),
    ]