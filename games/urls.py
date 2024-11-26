from django.urls import path

from .views import (GameCreateView, GameDeleteView, GameDetailView,
                    GameListView, GameSearchResultsView, GameUpdateView,
                    MyArchivedGameListView, archive_all_finished_games,
                    archive_finished_game, join_open_game, process_move,
                    stone_selector)

urlpatterns = [
    path("game_list/", GameListView.as_view(), name="game_list"),
    path("create/", GameCreateView.as_view(), name="game_create"),
    path("<uuid:pk>/", GameDetailView.as_view(), name="game_detail"),
    path("<uuid:pk>/update/", GameUpdateView.as_view(), name="game_update"),
    path("<uuid:pk>/delete/", GameDeleteView.as_view(), name="game_delete"),
    path("<uuid:pk>/join/", join_open_game, name="game_join"),
    path("<uuid:pk>/archive/", archive_finished_game, name="game_archive"),
    path("archive/all/", archive_all_finished_games, name="game_archive_all"),
    path(
        "archived_game_list/",
        MyArchivedGameListView.as_view(),
        name="my_archived_game_list",
    ),
    path(
        "process_move/<uuid:pk>/<int:stone>/<int:row>/<int:col>/",
        process_move,
        name="process_move",
    ),
    path(
        "select_stone/<uuid:pk>/<int:stone>/",
        stone_selector,
        name="select_stone",
    ),
    path("search/", GameSearchResultsView.as_view(), name="search"),
]
