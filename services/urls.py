from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='services_list'),
    path('create/', views.create_service, name='services_create'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
    path('<int:pk>/request_service/', views.request_service, name='request_service'),
    path('<slug:field>/', views.service_field, name='services_field'),
    path('most-requested/', views.most_requested, name='most_requested'),
]