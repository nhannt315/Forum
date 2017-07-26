# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 06:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid_term_mark', models.FloatField()),
                ('final_mark', models.FloatField()),
                ('status', models.CharField(choices=[('PS', 'PASS'), ('NP', 'NOT PASS')], default='NP', max_length=2)),
                ('avg_mark', models.FloatField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Marks',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('credit', models.IntegerField()),
                ('subject_id', models.CharField(max_length=8)),
                ('short_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Subjects',
            },
        ),
        migrations.AddField(
            model_name='mark',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mark', to='subjects.Subject'),
        ),
    ]