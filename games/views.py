from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
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
        player_id = self.object.player1.id
        return reverse_lazy("userprofile_detail", kwargs={"pk": player_id})

    def test_func(self):
        obj = self.get_object()
        return obj.player1 == self.request.user


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


class MoveValidationView(View):
    def post(self, request, *args, **kwargs):
        stone = request.POST.get("stone")
        row = request.POST.get("row")
        col = request.POST.get("col")
        game = Game.objects.get(pk=kwargs["game_id"])
        valid_move = game_rules.is_valid_move(game, stone, row, col)
        if valid_move:
            game = game_rules.assign_move(game, stone, row, col)
            game.save()
            # Update move list and cell
            move_list_html = render_to_string(
                "move_list.html", {"moves": game.moves.all()}
            )
            cell_html = render_to_string(
                "cell_template.html", {"game": game, "row": row, "col": col}
            )
            return JsonResponse(
                {
                    "valid": True,
                    "cell_html": cell_html,
                    "move_list_html": move_list_html,
                    "row": row,
                    "col": col,
                }
            )
        else:
            message = render_to_string(
                "message_template.html", {"message": "Invalid move"}
            )
            return JsonResponse({"valid": False, "message": message})


def process_move(request, pk, stone, row, col):
    game = Game.objects.get(pk=pk)
    valid_move = game_rules.is_valid_move(game, stone, row, col)
    if valid_move:
        game = game_rules.assign_move(game, stone, row, col)
        game.save()
    return redirect("game_detail", pk=pk)
