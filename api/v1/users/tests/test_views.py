from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CreateUserAPITests(TestCase):
    def test_register_user_success(self):
        payload = {
            "firstName": "Test",
            "lastName": "Account",
            "username": "testaccount",
            "email": "test.account@example.com",
            "password": "secret",
            "passwordConfirmation": "secret",
        }

        response = self.client.post(reverse("register_user"), payload)

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())


class LoginUserAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testaccount",
            email="test.account@example.com",
            password="secret",
            first_name="Test",
            last_name="Account",
        )

    def test_login_user_success(self):
        response = self.client.post(
            reverse("login_user"),
            {"username": self.user.username, "password": "secret"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertIn("user", response.json()["data"])
        self.assertEqual(response.json()["data"]["user"]["id"], self.user.id)


class AuthenticateUserAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testaccount",
            email="test.account@example.com",
            password="secret",
            first_name="Test",
            last_name="Account",
        )

    def test_authenticate_user_success(self):
        access_token = str(RefreshToken.for_user(self.user).access_token)

        response = self.client.get(
            reverse("authorise_user"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.json())


class LogoutUserAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testaccount",
            email="test.account@example.com",
            password="secret",
            first_name="Test",
            last_name="Account",
        )
        self.refresh_token = RefreshToken.for_user(self.user)

    def test_logout_user_success(self):
        response = self.client.post(
            reverse("logout_user"),
            {"refresh": str(self.refresh_token)},
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_token.access_token}",
        )

        self.assertEqual(response.status_code, 205)
        self.assertTrue(
            BlacklistedToken.objects.filter(
                token__jti=self.refresh_token["jti"]
            ).exists()
        )
