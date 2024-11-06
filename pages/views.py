from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import DetailView, ListView
from django.views.generic import TemplateView

from game_messages.models import Invitation
from games.models import Game


class HomePageView(ListView):
    model = get_user_model()
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        active_players = User.objects.filter(is_active=True)
        context["top_10_by_rating"] = active_players.order_by("-rating")[:10]
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
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["hosted_games"] = Game.objects.filter(player1=user)
        context["joined_games"] = Game.objects.filter(player2=user)
        context["invitation_list"] = Invitation.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )
        return context
