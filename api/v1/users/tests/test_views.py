from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterUserViewTests(TestCase):
    def test_register_user_post_is_allowed(self):
        payload = {
            "firstName": "Jane",
            "lastName": "Doe",
            "username": "janedoe",
            "email": "jane@example.com",
            "password": "secret123",
            "passwordConfirmation": "secret123",
        }

        response = self.client.post(reverse("register-user"), payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "janedoe")
        self.assertEqual(response.json()["email"], "jane@example.com")
        self.assertTrue(User.objects.filter(username="janedoe").exists())

    def test_register_user_post_returns_flattened_errors(self):
        payload = {
            "firstName": "",
            "lastName": "Doe",
            "username": "janedoe",
            "email": "jane@example.com",
            "password": "secret123",
            "passwordConfirmation": "secret123",
        }

        response = self.client.post(reverse("register-user"), payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["message"],
            "The first name field may not be blank.",
        )
        self.assertNotIn("errors", response.json())


class AuthoriseUserViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="janedoe",
            email="jane@example.com",
            password="secret123",
            first_name="Jane",
            last_name="Doe",
        )

    def test_authorise_user_get_returns_authenticated_user(self):
        access_token = str(RefreshToken.for_user(self.user).access_token)

        response = self.client.get(
            reverse("authorise_user"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"]["username"], "janedoe")
        self.assertEqual(response.json()["user"]["firstName"], "Jane")

    def test_authorise_user_get_requires_authentication(self):
        response = self.client.get(reverse("authorise_user"))

        self.assertEqual(response.status_code, 401)
