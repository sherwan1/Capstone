# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-17 22:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0012_grouppost'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('pub_date', models.DateTimeField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.Profile')),
                ('which_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.GroupPost')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='file_name',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='file_url',
            field=models.CharField(max_length=1500, null=True),
        ),
    ]