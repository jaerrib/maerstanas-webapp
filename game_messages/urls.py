from django.urls import path

from .views import (
    InvitationCreateView,
    accept_invitation,
    decline_invitation,
    InvitationListView,
    delete_system_notice,
    delete_all_system_notices_for_user,
)

urlpatterns = [
    path("invite/<uuid:receiver_pk>/", InvitationCreateView.as_view(), name="invite"),
    path(
        "invite/accept/<uuid:invitation_id>/",
        accept_invitation,
        name="accept_invitation",
    ),
    path(
        "invite/decline/<uuid:invitation_id>/",
        decline_invitation,
        name="decline_invitation",
    ),
    path("invitations/", InvitationListView.as_view(), name="invitations"),
    path("delete_notice/<uuid:notice_id>/", delete_system_notice, name="delete_notice"),
    path(
        "delete_all_notices/",
        delete_all_system_notices_for_user,
        name="delete_all_notices",
    ),
]
