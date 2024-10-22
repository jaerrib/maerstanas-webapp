from django.urls import path

from .views import (
    GameListView,
    GameDetailView,
    GameCreateView,
    GameUpdateView,
    GameDeleteView,
    join_open_game,
    MoveValidationView,
)

urlpatterns = [
    path("game_list/", GameListView.as_view(), name="game_list"),
    path("create/", GameCreateView.as_view(), name="game_create"),
    path("<uuid:pk>/", GameDetailView.as_view(), name="game_detail"),
    path("<uuid:pk>/update/", GameUpdateView.as_view(), name="game_update"),
    path("<uuid:pk>/delete/", GameDeleteView.as_view(), name="game_delete"),
    path("<uuid:pk>/join/", join_open_game, name="game_join"),
    path(
        "validate_move/<uuid:game_id>/",
        MoveValidationView.as_view(),
        name="validate_move",
    ),
]
