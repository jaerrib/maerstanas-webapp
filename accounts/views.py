from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView


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
