from django.urls import path

from .views import (
    InvitationCreateView,
    AcceptInvitationView,
    DeclineInvitationView,
    InvitationListView,
)

urlpatterns = [
    path("invite/<uuid:receiver_pk>/", InvitationCreateView.as_view(), name="invite"),
    path(
        "invite/accept/<uuid:invitation_id>/",
        AcceptInvitationView.as_view(),
        name="accept_invitation",
    ),
    path(
        "invite/decline/<uuid:invitation_id>/",
        DeclineInvitationView.as_view(),
        name="decline_invitation",
    ),
    path("invitations/", InvitationListView.as_view(), name="invitations"),
]
