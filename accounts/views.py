from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, UpdateView, DeleteView

from .forms import CustomUserChangeForm


class UserProfileListView(ListView):
    User = get_user_model()
    context_object_name = "profiles_list"
    template_name = "account/userprofile_list.html"

    def get_queryset(self):
        return get_user_model().objects.filter(is_active=True)


class UserProfileDetailView(DetailView):
    model = get_user_model()
    context_object_name = "player"
    template_name = "account/userprofile_detail.html"


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = "account/userprofile_update.html"

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    context_object_name = "account"
    template_name = "account/userprofile_delete.html"
    success_url = "/"

    def get_object(self, queryset=None):
        return self.request.user
