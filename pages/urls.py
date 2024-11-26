from django.urls import path

from .views import (
    HomePageView,
    DashboardPageView,
    AboutPageView,
    PrivacyPolicyPageView,
    TermsOfServicePageView,
    SupportPageView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("dashboard/", DashboardPageView.as_view(), name="dashboard"),
    path("privacy_policy/", PrivacyPolicyPageView.as_view(), name="privacy_policy"),
    path(
        "terms_of_service/", TermsOfServicePageView.as_view(), name="terms_of_service"
    ),
    path("support/", SupportPageView.as_view(), name="support"),
]
