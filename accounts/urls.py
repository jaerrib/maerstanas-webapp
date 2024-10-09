from django.urls import path

from .views import UserProfileDetailView, UserProfileListView

urlpatterns = [
    path("profiles/", UserProfileListView.as_view(), name="userprofile_list"),
    path(
        "profiles/<uuid:pk>/",
        UserProfileDetailView.as_view(),
        name="userprofile_detail",
    ),
]
