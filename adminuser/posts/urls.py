from django.urls import include, path
from .views import *


app_name = 'posts'
urlpatterns = [
    path('', home, name='home'),
    path('posts/', PostView.as_view(), name='posts'),
    path('user_page/', user_page, name='user_page'),
    path('ddd/', ddd, name='ddd'),


    # path('ddd/', ddd, name='ddd'),
    # path('register/', register, name='register'),
    # path('login/', login_user, name='login'),
    # path('logout/', logout_view, name='logout'),
]