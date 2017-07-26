# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='status',
            field=models.CharField(choices=[('ST', 'Studying'), ('GT', 'Graduated'), ('AD', 'Administrator')], default='ST', max_length=2),
        ),
    ]
