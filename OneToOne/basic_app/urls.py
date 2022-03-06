from turtle import fd
from django.urls import path, include
from basic_app import views
from django.contrib.auth import views as auth_views

app_name = 'basic_app'
urlpatterns = [
    path('register/', views.register, name='register'),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='myapp/login.html')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_page/', views.user_page, name='user_page'),
]