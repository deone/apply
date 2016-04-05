# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-05 10:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0012_auto_20160404_1117'),
        ('ashesiundergraduate', '0002_auto_20160403_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scholarships',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='setup.UserApplication')),
            ],
        ),
    ]
