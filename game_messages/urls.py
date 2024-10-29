from django.urls import path

from .views import InvitationCreateView

urlpatterns = [
    path("invite/<uuid:receiver_pk>/", InvitationCreateView.as_view(), name="invite"),
]
