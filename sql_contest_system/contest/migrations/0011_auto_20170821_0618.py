# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0010_auto_20170816_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task_submission',
            name='evaluation',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='\u041e\u0446\u0435\u043d\u043a\u0430'),
        ),
    ]