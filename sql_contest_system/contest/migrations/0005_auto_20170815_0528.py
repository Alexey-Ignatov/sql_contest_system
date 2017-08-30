# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 05:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_auto_20170808_2103'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleTaskSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('formulation', models.TextField(verbose_name='\u0424\u043e\u0440\u043c\u0443\u043b\u0438\u0440\u043e\u0432\u043a\u0430')),
                ('order_in_course', models.IntegerField(verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0437\u0430\u0434\u0430\u043d\u0438\u044f')),
            ],
            options={
                'ordering': ('order_in_course',),
                'verbose_name': '\u0417\u0430\u0434\u0430\u043d\u0438\u0435',
                'verbose_name_plural': '\u0417\u0430\u0434\u0430\u043d\u0438\u044f',
            },
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('title',), 'verbose_name': '\u0417\u0430\u0434\u0430\u0447\u0430', 'verbose_name_plural': '\u0417\u0430\u0434\u0430\u0447\u0430'},
        ),
        migrations.RemoveField(
            model_name='task',
            name='order_in_course',
        ),
        migrations.AlterField(
            model_name='task_deadline',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.ModuleTaskSet', verbose_name='\u0417\u0430\u0434\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='task_submission',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Task', verbose_name='\u0417\u0430\u0434\u0430\u0447\u0430'),
        ),
    ]
