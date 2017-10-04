
# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Task, Students_profile, Task_submission, Professor_profile, \
    Task_deadline_last, Task_deadline_first, Student_group, ModuleTaskSet,SubmissionGrade
from django.http import Http404
from .forms import SubmissionForm, AddUsersForm
from django.contrib import auth
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import pandas as pd
from datetime import datetime
import collections
from django.contrib.auth.models import User

import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO



import os
import zipfile

from django.http import HttpResponse


def get_subms(request, group_id, tasks_set_id):

    try:
        group = Student_group.objects.get(id = group_id)
    except group.DoesNotExist:
        raise Http404


    try:
        tasks_set = ModuleTaskSet.objects.get(id = tasks_set_id)
    except ModuleTaskSet.DoesNotExist:
        raise Http404



    students = Students_profile.objects.filter(student_group=group)
    dir_with_files_name =tasks_set.title +' ' +str(timezone.now())[:-13]
    os.mkdir(dir_with_files_name)

    all_sub_ids = []
    for student in students:
        subs = Task_submission.objects.filter(student=student)
        subs_info_list = []
        for sub in subs:
            if sub.task.module_task_set == tasks_set:

                sub_dict = {
                    'tasks_set': sub.task.module_task_set.title,
                    'task': sub.task.title,
                    'task_id': sub.task.id,
                    'subm_time': sub.subm_time,
                    'solution': sub.solution,
                    'sub_id':sub.id
                }
                subs_info_list.append(sub_dict)
                all_sub_ids.append(sub.id)

        subs_df = pd.DataFrame(subs_info_list) if subs_info_list else pd.DataFrame([], columns=['tasks_set', 'task',
                                                                                                'task_id', 'grade',
                                                                                                'subm_time', 'solution','sub_id'])
        subs_df = subs_df.sort_values('subm_time').groupby('task_id').last()
        subs_df = subs_df.set_index('sub_id')
        file_prefix =student.last_name + ' ' +  student.first_name + ' ' +  student.patronymic  + ' '

        for ind, row in subs_df.iterrows():
            fname = file_prefix + row['task']   +u' Id ' + str(ind) + u" .txt"

            with open(os.path.join(dir_with_files_name, fname), "w") as text_file:

                text_file.write(row['solution'].encode('utf-8') )


    pd.DataFrame([[i, -1] for i in all_sub_ids], columns = [u'Id решения', u'Оценка'])\
                                            .to_excel(os.path.join(dir_with_files_name, 'form_to_submit.xls'), index = False)
    filenames = [ os.path.join(dir_with_files_name, fname) for fname in os.listdir( dir_with_files_name )]

    zip_subdir = dir_with_files_name
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp




name_cols_to_viz = {'first_name': u'Имя',
             'last_name': u'Фамилия',
             'patronymic': u'Отчество',}

Row_tasks_list = collections.namedtuple('Row_tasks_list','task task_id tasks_set grade deadline1 deadline2')
Row_tasks_list_prof = collections.namedtuple('Row_tasks_list_prof','task task_id tasks_set grade deadline1 deadline2 first_name last_name patronymic')
@login_required(login_url='/auth/login')
def tasks_list(request):
    curr_user = auth.get_user(request)

    try:
        student = Students_profile.objects.get(system_user=curr_user)
    except SubmissionGrade.DoesNotExist:
        raise Http404


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
        try:
            grade = SubmissionGrade.objects.get(task_subm = sub).grade
        except SubmissionGrade.DoesNotExist:
            grade = u'На проверке'

        sub_dict = {
            'tasks_set':sub.task.module_task_set.title,
            'task':sub.task.title,
            'task_id': sub.task.id,
            'grade':grade,
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
    task_df = task_df.join(dl1_df.deadline.rename('deadline1'), on= 'tasks_set_id', how = 'right')
    task_df = task_df.join(dl2_df.deadline.rename('deadline2'), on= 'tasks_set_id')
    task_df.grade.fillna(u'Нет решений',inplace = True)
    task_df.deadline1.fillna(u'Не задан',inplace = True)
    task_df.deadline2.fillna(u'Не задан',inplace = True)


    #print(dl1_df.deadline.rename('deadline1'), 'dl1_df.deadline.rename')
    list_of_rows = [Row_tasks_list(task=r.loc['task'],
                        task_id=ind,
                        tasks_set=r.loc['tasks_set'],
                        grade=r.loc['grade'],
                        deadline1=r.loc['deadline1'],
                        deadline2=r.loc['deadline2'],
                        ) for ind, r in task_df.iterrows()]

    #print(task_df)
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

    try:
        d_line1 = Task_deadline_first.objects.get(group = student.student_group, task = task.module_task_set)
    except Task_deadline_first.DoesNotExist:
        return render(request, 'contest/task_details.html', {'task': task, 'form': None,'post':False,
                                                             'username': auth.get_user(request).username, })

    try:
        d_line2 = Task_deadline_last.objects.get(group = student.student_group, task = task.module_task_set)
    except Task_deadline_last.DoesNotExist:
        return render(request, 'contest/task_details.html', {'task': task, 'form': None,'post':False,
                                                             'username': auth.get_user(request).username, })




    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if (not Task_submission.objects.filter(student=student, task=task).exists() and timezone.now() < d_line1.deadline)\
        or timezone.now() > d_line2.deadline:
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
        return render(request, 'contest/task_details.html', {'task': task, 'form': None,'post':request.method == "POST",
                                                             'username': auth.get_user(request).username, })



def prof_home(request):
    groups = Student_group.objects.all()
    return render(request, 'contest/prof_home.html', {'username': auth.get_user(request).username, 'groups':groups})




@login_required(login_url='/auth/login')
def group_details(request, group_id):
    try:
        group = Student_group.objects.get(id = group_id)
    except Student_group.DoesNotExist:
        raise Http404

    tasks = Task.objects.all()
    subs = Task_submission.objects.all()
    students = Students_profile.objects.filter(student_group=group)

    d_lines_1 = Task_deadline_first.objects.filter(group=group)
    d_lines_2 = Task_deadline_last.objects.filter(group=group)

    students_list = []
    for stud in students:
        students_list.append({
            'student_id': stud.id,
            'first_name': stud.first_name,
            'last_name': stud.last_name,
            'patronymic': stud.patronymic,
        })


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
        try:
            grade = SubmissionGrade.objects.get(task_subm = sub).grade
        except SubmissionGrade.DoesNotExist:
            grade = u'На проверке'

        sub_dict = {
            'tasks_set': sub.task.module_task_set.title,
            'task': sub.task.title,
            'task_id': sub.task.id,
            'grade': grade,
            'subm_time': sub.subm_time,
            'student_id': sub.student.id
        }
        subs_info_list.append(sub_dict)

    tasks_info_list = []
    for task in tasks:
        task_dict = {
            'tasks_set': task.module_task_set.title,
            'tasks_set_id': task.module_task_set.id,
            'task': task.title,
            'task_id': task.id
        }
        tasks_info_list.append(task_dict)


    students_df = pd.DataFrame(students_list) if students_list  else pd.DataFrame([], columns=['student_id', 'first_name',
                                                                                               'last_name',
                                                                                               'patronymic'])

    dl1_df = pd.DataFrame(d_lines1_list) if d_lines1_list  else pd.DataFrame([], columns=['deadline', 'tasks_set_id'])
    dl1_df = dl1_df.set_index(u'tasks_set_id').fillna(u'Не задан')

    dl2_df = pd.DataFrame(d_lines2_list) if d_lines2_list  else pd.DataFrame([], columns=['deadline', 'tasks_set_id'])
    dl2_df = dl2_df.set_index(u'tasks_set_id').fillna(u'Не задан')

    task_df = pd.DataFrame(tasks_info_list) if tasks_info_list  else pd.DataFrame([], columns=['tasks_set', 'task',
                                                                                               'task_id',
                                                                                               'tasks_set_id'])
    #task_df.set_index(u'task_id', inplace=True)

    subs_df = pd.DataFrame(subs_info_list) if subs_info_list else pd.DataFrame([], columns=['tasks_set', 'task', 'task_id',
                                                                                        'grade', 'subm_time','student_id'])

    subs_df = subs_df.sort_values('subm_time').groupby(['student_id','task_id']).last().reset_index()

    task_df['dumm'] = 1
    students_df['dumm'] = 1

    out_df = pd.merge(students_df,task_df,  left_on='dumm',  right_on='dumm', how='outer')
    out_df = pd.merge(subs_df[['task_id','grade', 'student_id']], out_df, left_on=['task_id', 'student_id'], right_on= ['task_id', 'student_id'], how='outer')
    out_df = out_df.join(dl1_df.deadline.rename('deadline1'), on='tasks_set_id', how = 'right')
    out_df = out_df.join(dl2_df.deadline.rename('deadline2'), on='tasks_set_id')
    out_df.grade.fillna(u'Нет решений', inplace=True)
    out_df.deadline1.fillna(u'Не задан', inplace=True)
    out_df.deadline2.fillna(u'Не задан', inplace=True)


    transformed = out_df.pivot(index='student_id', columns='task_id', values='grade')
    task_final_names =  task_df.set_index('task_id').apply(lambda x: x.tasks_set + ' '+ x.task, 1)

    out_df = pd.merge(students_df, transformed, left_on='student_id', right_index=True, how='inner')

    out_df = out_df.drop(['student_id', 'dumm'], 1)
    out_df = out_df.sort_values(['last_name'])

    viz_names = []
    for x in out_df.columns:
        if x in task_final_names.index:
            viz_names.append((x, task_final_names[x], True))
        elif x in name_cols_to_viz:
            viz_names.append((x, name_cols_to_viz[x], False))
        else:
            viz_names.append((x, x, False))


    tasks_sets = task_df.groupby(['tasks_set_id', 'tasks_set']).first().index.tolist()
    return render(request, 'contest/group_details.html', {'tasks_sets':tasks_sets,
                                                            'tasks': out_df,
                                                          'group_id':group_id,
                                                          'col_names':viz_names,
                                                       'username': auth.get_user(request).username,
                                                       'subs': subs})







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
            return prof_home(request)
        except Professor_profile.DoesNotExist:
            return redirect('/auth/logout')




    return render(request, 'contest/prof_home.html', {'username': auth.get_user(request).username,})

@login_required(login_url='/auth/login')
def add_evals(request, group_id, task_id):
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

    try:
        group = Student_group.objects.get(id=group_id)
    except Student_group.DoesNotExist:
        raise Http404

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = AddUsersForm(request.POST)
        if form.is_valid():
            csv_str = form.cleaned_data.get('table')
            # now in the object cd, you have the form as a dictionary.
            df = pd.read_csv(StringIO(csv_str), sep="\t")
            df.columns = [i.decode('utf-8') for i in df.columns.tolist()]

            if not set([u'Id решения', u'Оценка']) <= set(df.columns.tolist()):
                return render(request, 'contest/message.html',
                              {'message': u'Введенные данные некорректны. Нет необходимых колонок.'})

            if df[u'Id решения'].unique().shape[0] != df[u'Id решения'].shape[0]:
                return render(request, 'contest/message.html',
                              {'message': u'Введенные данные некорректны. Номера студентов не уникальны.'})

            for ind, row in df.iterrows():

                try:
                    subm = Task_submission.objects.get(id = row[u'Id решения'])
                except Task_submission.DoesNotExist:
                    continue

                grade = SubmissionGrade(task_subm=subm,
                                        evaluation_date=timezone.now(),
                                        person = prof,
                                        grade = row[u'Оценка'])
                grade.save()
            return render(request, 'contest/message.html', {'message': u'Оценки заданы успешно'})
    else:
        form = AddUsersForm()

    return render(request, 'contest/add_grades.html', {'username': auth.get_user(request).username,
                                                         'form': form})


def add_students(request):
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


    if request.method=='POST':
        form = AddUsersForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #now in the object cd, you have the form as a dictionary.
            csv_str = cd.get('table')
            df = pd.read_csv(StringIO(csv_str), sep="\t")
            df.columns = [i.decode('utf-8') for i in df.columns.tolist()]

            if not set([u'Фамилия',u'Имя',u'Отчество', 'login','pswd',u'группа']) <=set(df.columns.tolist()):
                return render(request, 'contest/message.html', {'message':u'Введенные данные некорректны. Нет необходимых колонок.' })

            if df.login.unique().shape[0] != df.login.shape[0]:
                return render(request, 'contest/message.html', {'message':u'Введенные данные некорректны. Имена пользователей не уникальны.' })

            for ind, row in df.iterrows():

                try:
                    User.objects.get(username=row['login'])
                    return render(request, 'contest/message.html',
                                  {'message': u'Пользователь ' + str(row['login']) + u' уже существует'})
                except User.DoesNotExist:
                    pass

                user = User.objects.create_user(row['login'], '', row['pswd'])
                try:
                    group = Student_group.objects.get(title=row[u'группа'])
                except Student_group.DoesNotExist:
                    group = Student_group(title=row[u'группа'])
                group.save()
                student = Students_profile(first_name = row[u'Имя'],
                                           last_name=row[u'Фамилия'],
                                           patronymic=row[u'Отчество'],
                                           student_group=group,
                                           system_user = user
                                           )
                student.save()
            return render(request, 'contest/message.html', {'message': u'Пользователи созданы успешно'})
    else:
        form = AddUsersForm()


    return render(request, 'contest/add_students.html', {'username': auth.get_user(request).username,
                                                      'form':form})



