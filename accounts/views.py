from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from game_messages.models import Invitation
from games.models import Game
from .forms import CustomUserChangeForm


class UserProfileListView(LoginRequiredMixin, ListView):
    User = get_user_model()
    context_object_name = "profiles_list"
    template_name = "account/userprofile_list.html"

    def get_queryset(self):
        return (
            get_user_model()
            .objects.filter(is_active=True)
            .exclude(id=self.request.user.id)
            .order_by("-last_login")
        )


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    context_object_name = "player"
    template_name = "account/userprofile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        participating_games = Game.objects.filter(
            Q(player1=user, is_archived_for_p1=False)
            | Q(player2=user, is_archived_for_p2=False)
        )

        active_games = participating_games.exclude(player2=None).filter(game_over=False)
        context["total_active_games"] = active_games.count()
        open_game_sessions = participating_games.filter(Q(player1=user, player2=None))
        context["total_open_game_sessions"] = open_game_sessions.count()
        invitations = Invitation.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )
        context["total_invitations"] = invitations.count()
        return context


class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = "account/userprofile_update.html"

    def get_object(self):
        return self.request.user

    def test_func(self):
        return self.get_object() == self.request.user


class UserProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    context_object_name = "account"
    template_name = "account/userprofile_delete.html"
    success_url = "/"

    def get_object(self):
        return self.request.user

    def test_func(self):
        return self.get_object() == self.request.user


class PlayerSearchResultsView(LoginRequiredMixin, ListView):
    User = get_user_model()
    context_object_name = "player_list"
    template_name = "account/player_search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            player_list = get_user_model().objects.filter(
                Q(username__icontains=query), is_active=True
            )
        else:
            player_list = get_user_model().objects.none()
        return player_list
