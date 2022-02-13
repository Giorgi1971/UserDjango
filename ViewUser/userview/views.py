from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
# Create your views here.
 

# class LoginView()

def home(request):
    # return HttpResponse('This is Index')
    return render(request,'index.html')
    return redirect('userview:home')


def other(request):
    # return HttpResponse('This is other')
    return render(request,'other.html')


class UserPersonalView(DetailView):
    model = get_user_model()


class OtherView(ListView):
    model = get_user_model()



class RegisterView(CreateView):
    model = get_user_model()
    fields = '__all__'


# class LoginView()