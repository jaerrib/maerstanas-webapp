from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import GameCreateForm, GameUpdateForm
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


class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameCreateForm
    template_name = "game/game_create.html"

    def form_valid(self, form):
        form.instance.player1 = self.request.user
        return super().form_valid(form)


class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Game
    form_class = GameUpdateForm
    template_name = "game/game_update.html"

    def test_func(self):
        obj = self.get_object()
        return obj.player1 == self.request.user


class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Game
    template_name = "game/game_delete.html"

    def get_success_url(self):
        player_id = self.object.player1.id
        return reverse_lazy("userprofile_detail", kwargs={"pk": player_id})

    def test_func(self):
        obj = self.get_object()
        return obj.player1 == self.request.user


def join_open_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if game.player2 is None and game.player1 != request.user:
        game.player2 = request.user
        game.save()
        return redirect("game_detail", pk=game.pk)
    else:
        return redirect("home")
