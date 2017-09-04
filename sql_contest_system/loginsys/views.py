# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
#from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

#@csrf_protect
def login(request):
    args = {}
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            args['login_error'] = "Имя пользователя или пароль введены неверно"
            return render_to_response('login.html', args)

    else:
        return render_to_response('login.html', args)


@login_required(login_url='/auth/login')
def logout(request):
    auth.logout(request)
    return redirect('/auth/login')

