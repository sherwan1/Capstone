# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-20 03:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0022_auto_20180219_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='image',
        ),
        migrations.AddField(
            model_name='course',
            name='office_hours',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='office_location',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=1000),
        ),
    ]
