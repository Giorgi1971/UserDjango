from django.urls import include, path
from . views import *


app_name = 'account'
urlpatterns = [
    path('', index, name='index'),
    path('ttt/', ttt, name='ttt'),
    path('ddd/', ddd, name='ddd'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_view, name='logout'),
]