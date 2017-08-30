# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
#from django.views.decorators.csrf import csrf_protect

#@csrf_protect
def login(request):
    args = {}
    print "test"
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('tasks_list')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('login.html', args)

    else:
        return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('tasks_list')

