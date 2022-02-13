from django.urls import path, include
from .views import *


app_name = 'userview'
urlpatterns = [
    path('', home, name='home'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogOutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', UserPersonalView.as_view(), name='dashboard'),
    path('other/', other, name='other'),
]