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
    template_name = "games/game_list.html"


class GameDetailView(DetailView):
    model = Game
    context_object_name = "game"
    template_name = "games/game_detail.html"


class GameCreateView(CreateView):
    model = Game
    template_name = "games/game_create.html"


class GameUpdateView(UpdateView):
    model = Game
    template_name = "games/game_update.html"


class GameDeleteView(DeleteView):
    model = Game
    template_name = "games/game_delete.html"
