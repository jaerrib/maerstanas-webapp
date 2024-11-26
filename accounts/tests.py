from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .views import UserProfileListView, UserProfileDetailView


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", email="testuser@email.com", password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="superadmin", email="superadmin@email.com", password="testpass123"
        )
        self.assertEqual(user.username, "superadmin")
        self.assertEqual(user.email, "superadmin@email.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class SignUpPageTests(TestCase):
    username = "newuser"
    email = "newuser@email.com"

    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "Hello! I shouldn't be on the page")

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)


class PlayerProfilePageTests(TestCase):

    @classmethod
    def setUpClass(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="testuser", email="testuser@email.com", password="testpass123"
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_player_profile_page_for_logged_in_user(self):
        self.client.login(email="testuser@email.com", password="testpass123")
        self.response = self.client.get(self.user.get_absolute_url())
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/userprofile_detail.html")
        self.assertContains(self.response, "Player Profile")
        self.assertContains(self.response, "Record (W-L-T):")
        self.assertNotContains(self.response, "Hello! I should not be here.")
        view = resolve(f"/accounts/profiles/{self.user.pk}/")
        self.assertEqual(view.func.__name__, UserProfileDetailView.as_view().__name__)

    def test_player_profile_page_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.user.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"%s?next=/accounts/profiles/{self.user.pk}/" % (reverse("account_login")),
        )
        response = self.client.get(
            f"%s?next=/accounts/profiles/{self.user.pk}/" % (reverse("account_login")),
        )
        self.assertContains(response, "Log In")


class PlayerProfileListPageTests(TestCase):

    @classmethod
    def setUpClass(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="testuser", email="testuser@email.com", password="testpass123"
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_player_profile_list_page_for_logged_in_user(self):
        self.client.login(email="testuser@email.com", password="testpass123")
        url = reverse("userprofile_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/userprofile_list.html")
        self.assertContains(response, "Player List")
        self.assertNotContains(response, "Hello! I should not be here.")
        view = resolve(f"/accounts/profiles/")
        self.assertEqual(view.func.__name__, UserProfileListView.as_view().__name__)

    def test_player_profile_list_page_for_logged_out_user(self):
        self.client.logout()
        url = reverse("userprofile_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"%s?next=/accounts/profiles/" % (reverse("account_login")),
        )
        response = self.client.get(
            f"%s?next=/accounts/profiles/" % (reverse("account_login")),
        )
        self.assertContains(response, "Log In")
