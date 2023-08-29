from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('game/', views.game),
    path('new_game/<int:players>/', views.new_game),
    path('new_session/', views.new_session),
    path('reset/', views.reset),
    path('process/<int:row>/<int:col>/', views.process)
]
