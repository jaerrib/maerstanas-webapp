from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import DetailView, ListView, TemplateView

from game_messages.models import Invitation, SystemNotice
from games.models import Game


class HomePageView(ListView):
    model = get_user_model()
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        active_players = User.objects.filter(is_active=True)
        context["top_10_by_rating"] = active_players.order_by("-rating")[:10]
        context["total_active_players"] = active_players.count()
        game = Game
        context["total_active_games"] = (
            game.objects.filter(game_over=False).exclude(player2=None).count()
        )
        context["total_finished_games"] = game.objects.filter(game_over=True).count()
        return context


class AboutPageView(TemplateView):
    template_name = "about.html"


class PrivacyPolicyPageView(TemplateView):
    template_name = "privacy_policy.html"


class TermsOfServicePageView(TemplateView):
    template_name = "terms_of_service.html"


class SupportPageView(TemplateView):
    template_name = "support.html"


class DashboardPageView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "dashboard.html"
    context_object_name = "player"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        participating_games = Game.objects.filter(
            Q(player1=user, is_archived_for_p1=False)
            | Q(player2=user, is_archived_for_p2=False)
        )

        active_games = participating_games.exclude(player2=None).filter(game_over=False)
        context["active_games"] = active_games.order_by("name")
        context["total_active_games"] = active_games.count()

        completed_games = participating_games.filter(game_over=True)
        context["completed_games"] = completed_games.order_by("name")
        context["total_completed_games"] = completed_games.count()

        open_game_sessions = participating_games.filter(Q(player1=user, player2=None))
        context["open_game_sessions"] = open_game_sessions.order_by("name")
        context["total_open_game_sessions"] = open_game_sessions.count()

        invitations = Invitation.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )
        context["invitations"] = invitations
        context["total_invitations"] = invitations.count()

        system_notices = SystemNotice.objects.filter(user=self.request.user)
        context["system_notices"] = system_notices[::-1]
        context["total_system_notices"] = system_notices.count()

        return context
