from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="user index"),
    path('login/', views.login, name="login"),
    path('login/process/', views.login_process),
    path('registration/', views.registration, name="registration"),
    path('registration/process/', views.registration_process),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('host_new/', views.host_new, name="host new"),
    path('host_new/process/', views.host_new_process),
    path('open_games/', views.open_games, name="open games"),
    path('join_game/<str:game_name>/', views.join_game, name="join game"),
    path('private_game/process/', views.private_game_process),
    path('delete_game/<str:game_name>/', views.delete_game, name="delete game"),
    path('logout/', views.logout, name="logout"),
]
