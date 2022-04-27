from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('account:login'))


def index(request):
    u_message = 'About'
    return render(request, 'account/index.html', {'u_message': u_message})


def login_user(request):
    message = ''
    if request.method == 'POST':    
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('posts:user_page'))
        else:
            message = 'invalid credentials'
    return render(request, 'account/login.html', {'message': message})


def register(request):
    user_form = UserCreateForm()
    if request.method == 'POST':
        user_form = UserCreateForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.save()
            return HttpResponseRedirect(reverse('account:login'))

    return render(request, 'account/register.html', {'form': user_form})
