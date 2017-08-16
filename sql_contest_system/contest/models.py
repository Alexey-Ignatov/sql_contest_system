# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ModuleTaskSet(models.Model):
    title = models.CharField(verbose_name=u'Название', max_length=200)
    order_in_course = models.IntegerField(verbose_name=u'Номер задания')

    class Meta:
        ordering = ('order_in_course',)
        verbose_name = u'Задание'
        verbose_name_plural = u'Задания'

    def __unicode__(self):
        return self.title



class Task(models.Model):
    title = models.CharField(verbose_name=u'Название', max_length=200)
    formulation = models.TextField(verbose_name=u'Формулировка')
    module_task_set = models.ForeignKey(verbose_name=u'Задание', to=ModuleTaskSet)

    class Meta:
        ordering = ('title',)
        verbose_name = u'Задача'
        verbose_name_plural = u'Задача'

    def __unicode__(self):
        return self.module_task_set.title + ": " +  self.title





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
    DEADLINE_TYPES = (
        (0, u'Первый срок'),
        (1, u'Второй срок')
    )

    task = models.ForeignKey(verbose_name=u'Задание',to=ModuleTaskSet)
    group = models.ForeignKey(verbose_name=u'Группа', to=Student_group)
    deadline = models.DateTimeField(verbose_name=u'Срок сдачи')
    deadline_type = models.IntegerField(verbose_name=u'Вид срока', choices=DEADLINE_TYPES)

    class Meta:
        ordering = ('task', 'group')
        verbose_name = u'Срок сдачи'
        verbose_name_plural = u'Сроки сдачи'

    def __unicode__(self):
        return self.task.title + ' ' + str(self.group)


class Task_submission(models.Model):
    task = models.ForeignKey(verbose_name=u'Задача', to=Task)
    student = models.ForeignKey(verbose_name=u'Студент', to=Students_profile)

    solution = models.TextField(verbose_name=u'Решение')
    evaluation = models.PositiveIntegerField( verbose_name=u'Оценка',blank=True, default=None)
    class Meta:
        ordering = ('student', 'task')
        verbose_name = u'Посылка решения'
        verbose_name_plural = u'Посылки решения'

    def __unicode__(self):
        return self.student.__unicode__() + ' ' + self.task.__unicode__()
