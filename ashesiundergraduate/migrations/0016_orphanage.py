# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-08 22:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ashesiundergraduate', '0015_residence_living_with'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orphanage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name of orphanage')),
                ('contact_person_title', models.CharField(max_length=20, verbose_name='contact person title')),
                ('contact_person_name', models.CharField(max_length=50, verbose_name='contact person name')),
                ('contact_person_phone_number', models.CharField(max_length=15, verbose_name='contact person phone number')),
                ('contact_person_email', models.EmailField(max_length=254, verbose_name='contact person email address')),
                ('residence', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ashesiundergraduate.Residence')),
            ],
        ),
    ]
