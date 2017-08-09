# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin
from models import Student_group, Students_profile, Task, Task_deadline, Task_submission




admin.site.register(Students_profile)
admin.site.register(Student_group)
admin.site.register(Task_deadline)
admin.site.register(Task)
admin.site.register(Task_submission)
# Register your models here.
