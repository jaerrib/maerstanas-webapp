from django.views.generic import TemplateView


class InviteView(TemplateView):
    template_name = "messages/invitation.html"
