from django.urls import path

from .views import BotGameCreateView

urlpatterns = [
    path("create/", BotGameCreateView.as_view(),
         name="bot_game_create"),
]
