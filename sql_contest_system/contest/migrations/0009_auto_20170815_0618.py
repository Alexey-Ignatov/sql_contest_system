# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 06:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0008_auto_20170815_0608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='module_task_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.ModuleTaskSet', verbose_name='\u0417\u0430\u0434\u0430\u043d\u0438\u0435'),
        ),
    ]