from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('login/process/', views.login_process),
    path('registration/', views.registration),
    path('registration/process/', views.registration_process),
    path('dashboard/', views.dashboard),
    path('profile/', views.profile),
    path('host_new/', views.host_new),
    path('logout/', views.logout),
]
