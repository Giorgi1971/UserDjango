from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('account:login'))


def index(request):
    return render(request, 'account/index.html')


def login_user(request):
    if request.method == 'POST':    
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('posts:user_page'))
        else:
            # Return an 'invalid login' error message.
            return HttpResponseRedirect(reverse('posts:ddd'))
            ...
    return render(request, 'account/login.html')


def register(request):
    user_form = UserCreateForm()
    if request.method == 'POST':
        user_form = UserCreateForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.save()
            return HttpResponseRedirect(reverse('account:login'))

    return render(request, 'account/register.html', {'form':user_form})