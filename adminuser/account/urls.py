from django.urls import include, path
from . views import *


urlpatterns = [
    path('', index, name='index'),
    path('register', register, name='register'),
]