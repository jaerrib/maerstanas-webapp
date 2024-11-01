from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from games.logic import game_rules
from .forms import GameCreateForm, GameUpdateForm, PasswordForm
from .models import Game


class GameListView(LoginRequiredMixin, ListView):
    model = Game
    context_object_name = "game_list"
    template_name = "game/game_list.html"

    def get_queryset(self):
        return Game.objects.filter(player2=None)


class GameDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Game
    context_object_name = "game"
    template_name = "game/game_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "active_stone" not in self.request.session:
            self.request.session["active_stone"] = 1
        context["active_stone"] = self.request.session["active_stone"]
        return context

    def test_func(self):
        obj = self.get_object()
        return obj.player1 == self.request.user or obj.player2 == self.request.user


class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameCreateForm
    template_name = "game/game_create.html"

    def form_valid(self, form):
        form.instance.player1 = self.request.user
        response = super().form_valid(form)
        game = form.instance
        game_rules.initialize_game(game)
        game.save()
        return response


class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Game
    form_class = GameUpdateForm
    template_name = "game/game_update.html"

    def test_func(self):
        obj = self.get_object()
        return obj.player1 == self.request.user

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.object
        context["show_password_change"] = session.player2 is None
        return context


class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Game
    template_name = "game/game_delete.html"

    def get_success_url(self):
        return reverse_lazy("dashboard")

    def test_func(self):
        obj = self.get_object()
        return obj.player1 == self.request.user or obj.player2 == self.request.user

    def form_valid(self, form):
        game = self.get_object()
        if game.player2 is not None and not game.game_over:
            if game.player1 == self.request.user:
                game.player1.games_abandoned += 1
                game.player1.save()
            if game.player2 == self.request.user:
                game.player2.games_abandoned += 1
                game.player2.save()
        return super().form_valid(form)


def join_open_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if game.player1 == request.user or game.player2 == request.user:
        return redirect("game_detail", pk=pk)

    if game.password:
        if request.method == "POST":
            form = PasswordForm(request.POST)
            if form.is_valid():
                if game.check_password(form.cleaned_data["password"]):
                    game.player2 = request.user
                    game.save()
                    return redirect("game_detail", pk=pk)
                else:
                    form.add_error("password", "Incorrect password")
        else:
            form = PasswordForm()
        return render(request, "game/join_game.html", {"form": form, "game": game})
    else:
        game.player2 = request.user
        game.save()
        return redirect("game_detail", pk=pk)


def process_move(request, pk, stone, row, col):
    game = Game.objects.get(pk=pk)
    active_game = game.player2 is not None
    valid_move = game_rules.is_valid_move(game, stone, row, col)
    if not game.game_over and game_rules.player_must_pass(game):
        game = game_rules.pass_player_turn(game)
        game.save()
    elif (
        active_game
        and valid_move
        and (
            (game.active_player == 1 and game.player1 == request.user)
            or (game.active_player == 2 and game.player2 == request.user)
        )
    ):
        game = game_rules.assign_move(game, stone, row, col)
        game.moves_left_list = game_rules.remaining_standard_moves(
            game.gameboard["data"]
        )
        game = game_rules.update_score(game)
        game = game_rules.change_player(game)
        game.game_over = game_rules.is_game_over(game)
        if game.game_over:
            game = complete_game(game)
        game.save()
    return redirect("game_detail", pk=pk)


def stone_selector(request, pk, stone):
    if "active_stone" not in request.session:
        request.session["active_stone"] = 1
    else:
        request.session["active_stone"] = stone
    return redirect("game_detail", pk=pk)


def complete_game(game):
    game.result = game_rules.determine_winner(game.score_p1, game.score_p2)
    if game.result == "Player 1":
        game.player1.games_won += 1
        game.player1.save()
        game.player2.games_lost += 1
        game.player2.save()
    if game.result == "Player 2":
        game.player1.games_lost += 1
        game.player1.save()
        game.player2.games_won += 1
        game.player2.save()
    if game.result == "Tie":
        game.player1.games_tied += 1
        game.player1.save()
        game.player2.games_tied += 1
        game.player2.save()
    return game


class GameSearchResultsView(LoginRequiredMixin, ListView):
    model = Game
    template_name = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("search")
        special_stones = self.request.GET.get("special_stones")
        standard_scoring = self.request.GET.get("standard_scoring")
        game_list = Game.objects.filter(
            Q(name__icontains=query) | Q(player1__username__icontains=query),
            game_over=False,
            player2=None,
        )
        if special_stones:
            game_list = game_list.filter(using_special_stones=True)
        if standard_scoring:
            game_list = game_list.filter(using_standard_scoring=True)
        return game_list
