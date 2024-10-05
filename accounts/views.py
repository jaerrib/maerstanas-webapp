from django.views.generic import TemplateView


class PlayerProfilePageView(TemplateView):
    template_name = "account/player_profile.html"
