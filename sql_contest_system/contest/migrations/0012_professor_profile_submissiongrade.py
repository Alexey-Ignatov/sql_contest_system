# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 06:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0011_auto_20170821_0618'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='\u0418\u043c\u044f')),
                ('last_name', models.CharField(max_length=200, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f')),
            ],
            options={
                'ordering': ('first_name', 'last_name'),
                'verbose_name': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442',
                'verbose_name_plural': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='SubmissionGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation_date', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0446\u0435\u043d\u043a\u0438')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Professor_profile', verbose_name='\u0420\u0435\u0448\u0435\u043d\u0438\u0435')),
                ('task_subm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Task_submission', verbose_name='\u0420\u0435\u0448\u0435\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('task_subm', 'evaluation_date'),
                'verbose_name': '\u041e\u0446\u0435\u043d\u043a\u0430 \u0440\u0435\u0448\u0435\u043d\u0438\u044f',
                'verbose_name_plural': '\u041e\u0446\u0435\u043d\u043a\u0438',
            },
        ),
    ]
