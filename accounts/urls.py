from django.urls import path

from .views import PlayerProfilePageView

urlpatterns = [
    path("player_profile/", PlayerProfilePageView.as_view(), name="player_profile"),
]
