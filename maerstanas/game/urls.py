from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="homepage"),
    path('game/', views.game),
    path('new_game/<int:players>/', views.new_game, name="new guest"),
    path('new_session/', views.new_session, name="new session"),
    path('reset/', views.reset, name="reset"),
    path('process/<int:row>/<int:col>/', views.process)
]
