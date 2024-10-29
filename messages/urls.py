from django.urls import path

from .views import InviteView

urlpatterns = [
    path("invite/", InviteView.as_view(), name="invite"),
]
