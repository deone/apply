# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 12:55
from __future__ import unicode_literals

import ashesiundergraduate.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ashesiundergraduate', '0009_auto_20160407_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinformation',
            name='photo',
            field=models.ImageField(height_field='photo_height', help_text='File name must be in the format - Firstname_Lastname.jpg', upload_to=ashesiundergraduate.models.get_upload_path, width_field='photo_width'),
        ),
    ]
