from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.LoginUserView, name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('company/<int:user_id>/', views.company_profile, name='company_profile'),
]