import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UpdateUserViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="janedoe",
            email="jane@example.com",
            password="secret123",
            first_name="Jane",
            last_name="Doe",
        )
        self.access_token = str(RefreshToken.for_user(self.user).access_token)

    def patch_user(self, payload):
        return self.client.patch(
            reverse("web:users:logout_user"),
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

    def test_patch_updates_profile_and_password(self):
        response = self.patch_user(
            {
                "firstName": "Janet",
                "lastName": "Smith",
                "email": "janet@example.com",
                "password": "newsecret123",
                "passwordConfirmation": "newsecret123",
            }
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success."})
        self.assertEqual(self.user.first_name, "Janet")
        self.assertEqual(self.user.last_name, "Smith")
        self.assertEqual(self.user.email, "janet@example.com")
        self.assertTrue(self.user.check_password("newsecret123"))

    def test_patch_with_empty_password_preserves_current_password(self):
        response = self.patch_user(
            {
                "firstName": "Janet",
                "lastName": "Smith",
                "email": "janet@example.com",
                "password": "",
            }
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password("secret123"))

    def test_patch_with_missing_password_confirmation_fails(self):
        response = self.patch_user(
            {
                "firstName": "Janet",
                "lastName": "Smith",
                "email": "janet@example.com",
                "password": "newsecret123",
            }
        )

        self.assertEqual(response.status_code, 400)
