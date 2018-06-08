# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-20 02:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0020_course_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='coursecomment',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='coursecomment',
            name='which_post',
        ),
        migrations.RemoveField(
            model_name='coursefile',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursefile',
            name='uploaded_by',
        ),
        migrations.RemoveField(
            model_name='coursepost',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursepost',
            name='liked_by',
        ),
        migrations.RemoveField(
            model_name='coursepost',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='coursetable',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursetable',
            name='member',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='CourseComment',
        ),
        migrations.DeleteModel(
            name='CourseFile',
        ),
        migrations.DeleteModel(
            name='CoursePost',
        ),
        migrations.DeleteModel(
            name='CourseTable',
        ),
    ]