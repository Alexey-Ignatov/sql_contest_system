
# -*- coding: utf-8 -*-

from django.shortcuts import render


from django.shortcuts import render
from django.utils import timezone
from .models import Task, Students_profile
from django.http import Http404
from .forms import SubmissionForm

def tasks_list(request):
    tasks = Task.objects.all()
    return render(request, 'contest/tasks_list.html', {'tasks':tasks})


def task_details(request, task_id):

    try:
        task = Task.objects.get(id = task_id)
    except Task.DoesNotExist:
        print ('Task.DoesNotExist')
        raise Http404
    print task_id
    print type(task_id)
    print 'task_id'
    print type(u'0')
    print 'u0 type'
    try:
        student = Students_profile.objects.get(id = u'1')
    except Students_profile.DoesNotExist:
        print ('Students_profile.DoesNotExist')
        raise Http404

    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.task = task
            post.student = student
            post.save()

    else:
        form = SubmissionForm()


    return render(request, 'contest/task_details.html', {'task':task, 'form':form})




