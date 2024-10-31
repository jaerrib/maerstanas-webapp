from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, \
    View

from games.logic.game_rules import initialize_game
from games.models import Game
from .forms import InvitationCreateForm
from .models import Invitation

User = get_user_model()


class InviteView(TemplateView):
    template_name = "game_messages/invite.html"


class InvitationListView(LoginRequiredMixin, ListView):
    model = Invitation
    context_object_name = "invitation_list"
    template_name = "game_messages/invitation_list.html"

    def get_queryset(self):
        return Invitation.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )


class InvitationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Invitation
    context_object_name = "invitation_detail"
    template_name = "game_messages/invitation_detail.html"

    def test_func(self):
        obj = self.get_object()
        return obj.sender == self.request.user or obj.receiver == self.request.user


class InvitationCreateView(LoginRequiredMixin, CreateView):
    model = Invitation
    form_class = InvitationCreateForm
    template_name = "game_messages/invitation_create.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["receiver"] = User.objects.get(pk=self.kwargs["receiver_pk"])
        return context

    def form_valid(self, form):
        form.instance.sender = self.request.user
        receiver = User.objects.get(pk=self.kwargs["receiver_pk"])
        form.instance.receiver = receiver
        game_name = form.cleaned_data.get("game_name")
        using_special_stones = form.cleaned_data.get("using_special_stones")
        using_standard_scoring = form.cleaned_data.get("using_standard_scoring")
        new_game = Game.objects.create(
            name=game_name,
            player1=self.request.user,
            player2=receiver,
            using_special_stones=using_special_stones,
            using_standard_scoring=using_standard_scoring,
        )
        if not using_special_stones:
            new_game.p1_has_thunder_stone = False
            new_game.p1_has_woden_stone = False
            new_game.p2_has_thunder_stone = False
            new_game.p2_has_woden_stone = False
        new_game = initialize_game(new_game)
        new_game.save()
        form.instance.game = new_game
        return super().form_valid(form)


class AcceptInvitationView(View):
    def post(self, request, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)
        invitation.approved = True
        invitation.save()
        return redirect(invitation.game.get_absolute_url())


class DeclineInvitationView(View):
    def post(self, request, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)
        game = invitation.game
        sender = invitation.sender
        invitation.delete()
        game.delete()
        messages.add_message(
            request, messages.INFO, f"{sender.username}, your invitation was declined."
        )
        return redirect("invitations")