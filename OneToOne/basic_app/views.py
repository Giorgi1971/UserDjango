from django.shortcuts import render
from .forms import *
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'basic_app/index.html')


# @login_required(redirect_field_name='user_page')
def user_page(request):
    return render(request, 'basic_app/user_page.html')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('basic_app:user_page'))
            ...
        else:
            # Return an 'invalid login' error message.
            messages = 'invalid login'
            print(messages)
            return render(request, 'basic_app/login.html', {'messages':messages})
    else:
        return render(request, 'basic_app/login.html')


def register(request):
    registered = False

    if request.method == 'POST':
        print('post')
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered =True
            print('regis')

        else:
            print(user_form.errors, profile_form.errors)
    else:
        print('no post')
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/register.html', {'user_form':user_form,
                                                    'profile_form':profile_form,
                                                    'registered':registered })
