# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin
from models import Student_group, Students_profile, Task, Task_deadline_first, \
    Task_submission, ModuleTaskSet, SubmissionGrade, Professor_profile, Task_deadline_last




admin.site.register(Students_profile)
admin.site.register(Student_group)
admin.site.register(Task_deadline_first)
admin.site.register(Task_deadline_last)
admin.site.register(Task)
admin.site.register(Task_submission)
admin.site.register(ModuleTaskSet)
admin.site.register(SubmissionGrade)
admin.site.register(Professor_profile)
# Register your models here.
