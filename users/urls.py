from django.urls import path
from django.contrib.auth import views

from .forms import UserLoginForm
from . import views as v

urlpatterns = [
    path('', v.register, name='register'),
        path('login/', v.LoginUserView, name='login_user'),
        path('profile/', v.profile_view, name='profile')
]
