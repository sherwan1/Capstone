# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0008_message_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message_notification',
            name='notification_by_email',
            field=models.CharField(max_length=1000),
        ),
    ]
