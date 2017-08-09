# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 08:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20170729_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.TextField(verbose_name='\u0420\u0435\u0448\u0435\u043d\u0438\u0435')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Students_profile', verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Task', verbose_name='\u0417\u0430\u0434\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('student', 'task'),
                'verbose_name': '\u041f\u043e\u0441\u044b\u043b\u043a\u0430 \u0440\u0435\u0448\u0435\u043d\u0438\u044f',
                'verbose_name_plural': '\u041f\u043e\u0441\u044b\u043b\u043a\u0438 \u0440\u0435\u0448\u0435\u043d\u0438\u044f',
            },
        ),
    ]
