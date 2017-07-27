# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 03:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0004_auto_20170727_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='thread_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]