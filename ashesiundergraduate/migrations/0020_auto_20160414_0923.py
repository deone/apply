# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 09:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0013_auto_20160407_1131'),
        ('ashesiundergraduate', '0019_auto_20160413_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='course name')),
            ],
        ),
        migrations.CreateModel(
            name='DesiredMajor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ashesiundergraduate.Course')),
                ('user_application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='setup.UserApplication')),
            ],
        ),
        migrations.RemoveField(
            model_name='scholarships',
            name='user_application',
        ),
        migrations.DeleteModel(
            name='Scholarships',
        ),
    ]
