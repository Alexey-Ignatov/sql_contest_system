# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(verbose_name=u'Название', max_length=200)
    formulation = models.TextField(verbose_name=u'Формулировка')
    order_in_course = models.IntegerField(verbose_name=u'Номер задания')

    class Meta:
        ordering = ('order_in_course',)
        verbose_name = u'Задание'
        verbose_name_plural = u'Задания'

    def __unicode__(self):
        return self.title



class Student_group(models.Model):
    number = models.IntegerField(verbose_name=u'Номер группы')

    class Meta:
        ordering = ('number',)
        verbose_name = u'Группа'
        verbose_name_plural = u'Группы'

    def __unicode__(self):
        return str(self.number)



class Students_profile(models.Model):
    first_name = models.CharField(verbose_name=u'Имя', max_length=200)
    last_name = models.CharField(verbose_name=u'Фамилия', max_length=200)

    student_group = models.ForeignKey(to=Student_group)

    class Meta:
        ordering = ('first_name', 'last_name')
        verbose_name = u'Студент'
        verbose_name_plural = u'Студенты'

    def __unicode__(self):
        return self.first_name +' ' +self.last_name


class Task_deadline(models.Model):
    task = models.ForeignKey(verbose_name=u'Задание',to=Task)
    group = models.ForeignKey(verbose_name=u'Группа', to=Student_group)
    deadline = models.DateTimeField(verbose_name=u'Срок сдачи')

    class Meta:
        ordering = ('task', 'group')
        verbose_name = u'Срок сдачи'
        verbose_name_plural = u'Сроки сдачи'

    def __unicode__(self):
        return self.task.title + ' ' + str(self.group)


class Task_submission(models.Model):
    task = models.ForeignKey(verbose_name=u'Задание', to=Task)
    student = models.ForeignKey(verbose_name=u'Студент', to=Students_profile)

    solution = models.TextField(verbose_name=u'Решение')

    class Meta:
        ordering = ('student', 'task')
        verbose_name = u'Посылка решения'
        verbose_name_plural = u'Посылки решения'

    def __unicode__(self):
        return self.student.__unicode__() + ' ' + self.task.__unicode__()
