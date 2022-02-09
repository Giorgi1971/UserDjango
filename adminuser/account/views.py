from audioop import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import *
# Create your views here.


def index(request):
    return render(request, 'account/index.html')


def register(request):
    user_form = UserCreateForm()
    if request.method == 'POST':
        user_form = UserCreateForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # user.set_password(user.password1)
            user.save()
        return render(request, 'account/index.html') 

    return render(request, 'account/register.html', {'form':user_form})
