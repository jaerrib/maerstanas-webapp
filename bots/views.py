from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
)

from bots import forms
from games.logic import game_rules
from games.models import Game


class BotGameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = forms.BotGameCreateForm
    template_name = "bots/game_create.html"

    def form_valid(self, form):
        form.instance.player1 = self.request.user
        response = super().form_valid(form)
        game = form.instance
        game_rules.initialize_game(game)
        game.save()
        return response
