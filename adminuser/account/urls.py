from django.urls import path
from .views import *


app_name = 'account'
urlpatterns = [
    path('', index, name='about'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_view, name='logout'),
]
