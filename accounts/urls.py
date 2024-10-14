from django.urls import path

from .views import (
    UserProfileDetailView,
    UserProfileListView,
    UserProfileUpdateView,
    UserProfileDeleteView,
)

urlpatterns = [
    path("profiles/", UserProfileListView.as_view(), name="userprofile_list"),
    path(
        "profiles/<uuid:pk>/",
        UserProfileDetailView.as_view(),
        name="userprofile_detail",
    ),
    path(
        "profiles/<uuid:pk>/update/",
        UserProfileUpdateView.as_view(),
        name="userprofile_update",
    ),
    path(
        "profiles/<uuid:pk>/delete/",
        UserProfileDeleteView.as_view(),
        name="userprofile_delete",
    ),
]
