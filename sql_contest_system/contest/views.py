
# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Task, Students_profile, Task_submission, Professor_profile, \
    Task_deadline_last, Task_deadline_first
from django.http import Http404
from .forms import SubmissionForm
from django.contrib import auth
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import pandas as pd
from datetime import datetime
import collections
Row = collections.namedtuple('Row','task task_id tasks_set grade deadline1 deadline2')

@login_required(login_url='/auth/login')
def tasks_list(request):
    curr_user = auth.get_user(request)
    student = Students_profile.objects.get(system_user = curr_user)
    tasks = Task.objects.all()
    subs = Task_submission.objects.filter(student = student)

    d_lines_1 = Task_deadline_first.objects.filter(group = student.student_group)
    d_lines_2 = Task_deadline_last.objects.filter(group = student.student_group)

    d_lines1_list = []
    for dl in d_lines_1:
        d_lines1_list.append({
            'tasks_set_id': dl.task.id,
            'deadline': dl.deadline
        })

    d_lines2_list = []
    for dl in d_lines_2:
        d_lines2_list.append({
            'tasks_set_id': dl.task.id,
            'deadline': dl.deadline
        })

    subs_info_list = []
    for sub in subs:
        sub_dict = {
            'tasks_set':sub.task.module_task_set.title,
            'task':sub.task.title,
            'task_id': sub.task.id,
            'grade':sub.evaluation.grade if sub.evaluation else -1,
            'subm_time':sub.subm_time
        }
        subs_info_list.append(sub_dict)

    tasks_info_list = []
    for task in tasks:

        task_dict = {
            'tasks_set':task.module_task_set.title,
            'tasks_set_id': task.module_task_set.id,
            'task':task.title,
            'task_id':task.id
        }
        tasks_info_list.append(task_dict)


    dl1_df = pd.DataFrame(d_lines1_list) if d_lines1_list  else pd.DataFrame([], columns=['deadline', 'tasks_set_id'])
    dl1_df = dl1_df.set_index(u'tasks_set_id').fillna(u'Не задан')



    dl2_df = pd.DataFrame(d_lines2_list) if d_lines2_list  else pd.DataFrame([], columns=['deadline', 'tasks_set_id'])
    dl2_df = dl2_df.set_index(u'tasks_set_id').fillna(u'Не задан')


    task_df = pd.DataFrame(tasks_info_list) if tasks_info_list  else pd.DataFrame([], columns=['tasks_set','task', 'task_id', 'tasks_set_id'])
    task_df.set_index(u'task_id', inplace=True)

    subs_df = pd.DataFrame(subs_info_list)  if subs_info_list else pd.DataFrame([], columns=['tasks_set','task', 'task_id','grade','subm_time'])
    subs_df = subs_df.sort_values('subm_time').groupby('task_id').last()


    task_df = task_df.join(subs_df.grade)
    task_df = task_df.join(dl1_df.deadline.rename('deadline1'), on= 'tasks_set_id')
    task_df = task_df.join(dl2_df.deadline.rename('deadline2'), on= 'tasks_set_id')

    print(dl1_df.deadline.rename('deadline1'), 'dl1_df.deadline.rename')
    list_of_rows = [Row(task=r.loc['task'],
                        task_id=ind,
                        tasks_set=r.loc['tasks_set'],
                        grade=r.loc['grade'],
                        deadline1=r.loc['deadline1'],
                        deadline2=r.loc['deadline2'],
                        ) for ind, r in task_df.iterrows()]

    print(task_df)
    return render(request, 'contest/tasks_list.html', {'tasks':list_of_rows,
                                                       'username': auth.get_user(request).username,
                                                       'student': student,
                                                       'subs':subs})

@login_required(login_url='/auth/login')
def task_details(request, task_id):
    try:
        task = Task.objects.get(id = task_id)
    except Task.DoesNotExist:
        raise Http404


    curr_user = auth.get_user(request)
    try:
        student = Students_profile.objects.get(system_user=curr_user)
    except Students_profile.DoesNotExist:
        raise Http404

    d_line1 = Task_deadline_first.objects.get(group = student.student_group, task = task.module_task_set)
    d_line2 = Task_deadline_last.objects.get(group = student.student_group, task = task.module_task_set)



    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.task = task
            post.subm_time = timezone.now()
            post.student = student
            post.save()

    else:
        form = SubmissionForm()


    if (not Task_submission.objects.filter(student=student, task=task).exists() and timezone.now() < d_line1.deadline)\
        or timezone.now() > d_line2.deadline:
        return render(request, 'contest/task_details.html', {'task':task, 'form':form,
                                                       'username': auth.get_user(request).username,})
    else:
        return render(request, 'contest/task_details.html', {'task': task, 'form': None,
                                                             'username': auth.get_user(request).username, })


@login_required(login_url='/auth/login')
def home(request):
    curr_user = auth.get_user(request)

    try:
        student = Students_profile.objects.get(system_user=curr_user)
        if student:
            return redirect('tasks_list')
    except Students_profile.DoesNotExist:
        try:
            prof = Professor_profile.objects.get(system_user=curr_user)
        except Professor_profile.DoesNotExist:
            return redirect('/auth/logout')
            raise Http404



    return render(request, 'contest/prof_home.html', {'username': auth.get_user(request).username,})


