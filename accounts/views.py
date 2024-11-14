from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

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
