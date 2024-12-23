from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve

from .views import HomePageView, AboutPageView, DashboardPageView


class HomePageTests(TestCase):
    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "home.html")

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "Home")

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hello")

    def test_url_resolves_home_page_view(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("about")
        self.response = self.client.get(url)

    def test_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_about_page_template(self):
        self.assertTemplateUsed(self.response, "about.html")

    def test_about_page_contains_correct_html(self):
        self.assertContains(self.response, "About")

    def test_about_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hello")

    def test_url_resolves_about_page_view(self):
        view = resolve("/about/")
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)


class PrivacyPolicyPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("privacy_policy")
        self.response = self.client.get(url)

    def test_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_privacy_policy_page_template(self):
        self.assertTemplateUsed(self.response, "privacy_policy.html")

    def test_privacy_policy_page_contains_correct_html(self):
        self.assertContains(self.response, "Privacy Policy")

    def test_privacy_policy_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hello")

    def test_url_resolves_test_privacy_policy_page_view(self):
        view = resolve("/privacy_policy/")
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)


class TermsOfServicePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("terms_of_service")
        self.response = self.client.get(url)

    def test_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_terms_of_service_page_template(self):
        self.assertTemplateUsed(self.response, "terms_of_service.html")

    def test_terms_of_service_page_contains_correct_html(self):
        self.assertContains(self.response, "Terms of Service")

    def test_terms_of_service_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hello")

    def test_url_resolves_terms_of_service_page_view(self):
        view = resolve("/terms_of_service/")
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)


class SupportPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("support")
        self.response = self.client.get(url)

    def test_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_support_page_template(self):
        self.assertTemplateUsed(self.response, "support.html")

    def test_support_page_contains_correct_html(self):
        self.assertContains(self.response, "Support")

    def test_support_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hello")

    def test_url_resolves_support_page_view(self):
        view = resolve("/support/")
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)


class DashboardPageTests(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", email="testuser@email.com", password="testpass123"
        )
        url = reverse("dashboard")
        self.client.login(email="testuser@email.com", password="testpass123")
        self.response = self.client.get(url)

    def test_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_dashboard_page_template(self):
        self.assertTemplateUsed(self.response, "dashboard.html")

    def test_dashboard_page_contains_correct_html(self):
        self.assertContains(self.response, "Dashboard")

    def test_dashboard_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hello")

    def test_url_resolves_dashboard_page_view(self):
        view = resolve("/dashboard/")
        self.assertEqual(view.func.__name__, DashboardPageView.as_view().__name__)
