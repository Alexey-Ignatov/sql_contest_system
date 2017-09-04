# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

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
    last_name  = models.CharField(verbose_name=u'Фамилия', max_length=200)
    patronymic = models.CharField(verbose_name=u'Фамилия', max_length=200)

    student_group = models.ForeignKey(to=Student_group)
    system_user = models.OneToOneField(to=User)

    class Meta:
        ordering = ('first_name', 'last_name')
        verbose_name = u'Студент'
        verbose_name_plural = u'Студенты'

    def __unicode__(self):
        return self.first_name +' ' +self.last_name




class Professor_profile(models.Model):
    first_name = models.CharField(verbose_name=u'Имя', max_length=200)
    last_name = models.CharField(verbose_name=u'Фамилия', max_length=200)
    patronymic = models.CharField(verbose_name=u'Фамилия', max_length=200)

    system_user = models.OneToOneField(to=User)
    class Meta:
        ordering = ('first_name', 'last_name')
        verbose_name = u'Преподаватель'
        verbose_name_plural = u'Преподаватели'

    def __unicode__(self):
        return self.first_name +' ' +self.last_name



class Task_deadline_first(models.Model):

    task = models.ForeignKey(verbose_name=u'Задание',to=ModuleTaskSet)
    group = models.ForeignKey(verbose_name=u'Группа', to=Student_group)
    deadline = models.DateTimeField(verbose_name=u'Срок сдачи')


    class Meta:
        ordering = ('task', 'group')
        verbose_name = u'Первый срок сдачи'
        verbose_name_plural = u'Первые сроки'

    def __unicode__(self):
        return self.task.title + ' ' + str(self.group)


class Task_deadline_last(models.Model):
    task = models.ForeignKey(verbose_name=u'Задание',to=ModuleTaskSet)
    group = models.ForeignKey(verbose_name=u'Группа', to=Student_group)
    deadline = models.DateTimeField(verbose_name=u'Срок сдачи')


    class Meta:
        ordering = ('task', 'group')
        verbose_name = u'Второй срок сдачи'
        verbose_name_plural = u'Вторые сроки'

    def __unicode__(self):
        return self.task.title + ' ' + str(self.group)



class Task_submission(models.Model):
    task = models.ForeignKey(verbose_name=u'Задача', to=Task)
    student = models.ForeignKey(verbose_name=u'Студент', to=Students_profile)

    solution = models.TextField(verbose_name=u'Решение')
    evaluation = models.PositiveIntegerField( verbose_name=u'Оценка',blank=True, null=True)
    subm_time = models.DateTimeField(verbose_name=u'Время отправки')

    class Meta:
        ordering = ('student', 'task')
        verbose_name = u'Посылка решения'
        verbose_name_plural = u'Посылки решения'

    def __unicode__(self):
        return self.student.__unicode__() + ' ' + self.task.__unicode__()




class SubmissionGrade(models.Model):
    task_subm = models.ForeignKey(verbose_name=u'Решение', to=Task_submission)
    evaluation_date = models.DateTimeField(verbose_name=u'Дата оценки')

    person = models.ForeignKey(verbose_name=u'Преподаватель', to=Professor_profile)

    grade = models.PositiveIntegerField(verbose_name=u'Оценка')

    class Meta:
        ordering = ('task_subm', 'evaluation_date')
        verbose_name = u'Оценка решения'
        verbose_name_plural = u'Оценки'

    def __unicode__(self):
        return self.task_subm.__unicode__() + ' ' + self.evaluation_date.__unicode__()