from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import TemplateView

from games.models import Game


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


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
        return context
