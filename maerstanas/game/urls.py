from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="homepage"),
    path('guest_game/', views.guest_game, name="guest game"),
    path('new_game/<int:players>/', views.new_game, name="new guest"),
    path('new_session/', views.new_session, name="new session"),
    path(
        'session_game/<str:game_name>',
        views.session_game,
        name="session game"
    ),
    path(
        'session_game/process/<str:game_name>/<int:row>/<int:col>/',
        views.session_game_process,
        name="session game process"
    ),
    path('reset/', views.reset, name="reset"),
    path('process/<int:row>/<int:col>/', views.process, name="process")
]
