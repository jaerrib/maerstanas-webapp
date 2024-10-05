from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import HomePageView, AboutPageView, DashboardPageView


class HomePageTests(SimpleTestCase):
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


class DashboardPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("dashboard")
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
