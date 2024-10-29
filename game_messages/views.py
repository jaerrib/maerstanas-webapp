from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
)
from django.views.generic import TemplateView

from games.logic.game_rules import initialize_game
from games.models import Game
from .forms import InvitationCreateForm
from .models import Invitation

User = get_user_model()


class InviteView(TemplateView):
    template_name = "messages/invite.html"


class InvitationListView(LoginRequiredMixin, ListView):
    model = Invitation
    context_object_name = "invitation_list"
    template_name = "messages/invitation_list.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return Invitation.objects.filter(
            creator=self.request.user, receiver=self.request.user
        )


class InvitationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Invitation
    context_object_name = "invitation_detail"
    template_name = "game_messages/invitation_detail.html"

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user or obj.receiver == self.request.user


from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Invitation


class InvitationCreateView(LoginRequiredMixin, CreateView):
    model = Invitation
    form_class = InvitationCreateForm
    template_name = "game_messages/invitation_create.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.sender = self.request.user
        receiver = User.objects.get(pk=self.kwargs["receiver_pk"])
        form.instance.receiver = receiver
        game_name = form.cleaned_data.get("game_name")
        new_game = Game.objects.create(
            name=game_name, player1=self.request.user, player2=receiver
        )
        new_game = initialize_game(new_game)
        new_game.save()
        form.instance.game = new_game
        return super().form_valid(form)
