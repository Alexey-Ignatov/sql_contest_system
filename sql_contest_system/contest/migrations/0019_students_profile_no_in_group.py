# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-26 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0018_auto_20170926_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='students_profile',
            name='no_in_group',
            field=models.IntegerField(default=1, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0432 \u0433\u0440\u0443\u043f\u043f\u0435'),
            preserve_default=False,
        ),
    ]
