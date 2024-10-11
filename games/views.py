from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Game


class GameListView(ListView):
    model = Game
    context_object_name = "game_list"
    template_name = "game/game_list.html"

    def get_queryset(self):
        return Game.objects.filter(player2=None)


class GameDetailView(DetailView):
    model = Game
    context_object_name = "game"
    template_name = "game/game_detail.html"


class GameCreateView(CreateView):
    model = Game
    template_name = "game/game_create.html"


class GameUpdateView(UpdateView):
    model = Game
    template_name = "game/game_update.html"


class GameDeleteView(DeleteView):
    model = Game
    template_name = "game/game_delete.html"


def join_open_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if game.player2 is None and game.player1 != request.user:
        game.player2 = request.user
        game.save()
        return redirect("game_detail", pk=game.pk)
    else:
        return redirect("home")
