
# -*- coding: utf-8 -*-

from django.shortcuts import render


from django.shortcuts import render
from django.utils import timezone
from .models import Task, Students_profile, Task_submission
from django.http import Http404
from .forms import SubmissionForm
from django.contrib import auth
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import pandas as pd
from datetime import datetime
import collections


@login_required(login_url='/auth/login')
def tasks_list(request):
    curr_user = auth.get_user(request)
    student = Students_profile.objects.get(system_user = curr_user)
    tasks = Task.objects.all()
    subs = Task_submission.objects.filter(student = student)

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
            'task':task.title,
            'task_id':task.id
        }
        tasks_info_list.append(task_dict)


    task_df = pd.DataFrame(tasks_info_list) if tasks_info_list else pd.DataFrame()

    task_df.set_index(u'task_id', inplace=True)

    subs_df = pd.DataFrame(subs_info_list)  if subs_info_list  else pd.DataFrame()

    subs_df = subs_df.sort_values('subm_time').groupby('task_id').last()


    task_df = task_df.join(subs_df.grade)


    Row = collections.namedtuple('Row','task task_id tasks_set grade')

    print([r for ind, r in task_df.iterrows()])

    list_of_rows = [Row(task=r.loc['task'], task_id=ind, tasks_set=r.loc['tasks_set'], grade=r.loc['grade']) for ind, r in task_df.iterrows()]
    print (list_of_rows, '\n\n\n\n\n\n\n')
    #print(pd.DataFrame(subs_info_list))
    #tasks_df = pd.DataFrame(list(tasks.values()))
    #subs_df =pd.DataFrame(list(subs.values()))
    #print(subs_df)
    #print(tasks_df)
    #table = pd.DataFrame([[1,3],[1, 2]]).to_html()
    tasks = Task.objects.all()

    return render(request, 'contest/tasks_list.html', {'tasks':list_of_rows,
                                                       'username': auth.get_user(request).username,
                                                       'student': student,
                                                       'subs':subs})

@login_required(login_url='/auth/login')
def task_details(request, task_id):
    try:
        task = Task.objects.get(id = task_id)
    except Task.DoesNotExist:
        print ('Task.DoesNotExist')
        raise Http404

    try:
        curr_user = auth.get_user(request)
        student = Students_profile.objects.get(system_user=curr_user)
    except Students_profile.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.task = task
            post.subm_time = datetime.now()
            post.student = student
            post.save()

    else:
        form = SubmissionForm()


    return render(request, 'contest/task_details.html', {'task':task, 'form':form})




