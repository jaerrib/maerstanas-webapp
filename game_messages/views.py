from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
)
from django.views.generic import TemplateView

from .forms import InvitationCreateForm
from .models import Invitation


class InviteView(TemplateView):
    template_name = "messages/invite.html"


class InvitationListView(LoginRequiredMixin, ListView):
    model = Invitation
    context_object_name = "invitation_list"
    template_name = "messages/invitation_list.html"

    def get_queryset(self):
        return Invitation.objects.filter(
            creator=self.request.user, receiver=self.request.user
        )


class InvitationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Invitation
    context_object_name = "invitation_detail"
    template_name = "messages/invitation_detail.html"

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user or obj.receiver == self.request.user


class InvitationCreateView(LoginRequiredMixin, CreateView):
    model = Invitation
    form_class = InvitationCreateForm
    template_name = "messages/invitation_create.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = get_user_model().objects.get(
            id=self.kwargs["receiver_uuid"]
        )
        response = super().form_valid(form)
        invitation = form.instance
        invitation.save()
        return response
