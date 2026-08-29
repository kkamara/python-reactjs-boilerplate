from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class GetUsersViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="viewer",
            email="viewer@example.com",
            password="secret123",
            first_name="View",
            last_name="User",
        )
        for index in range(8):
            User.objects.create_user(
                username=f"user{index}",
                email=f"user{index}@example.com",
                password="secret123",
                first_name="Test",
                last_name=f"User{index}",
            )
        self.access_token = str(RefreshToken.for_user(self.user).access_token)

    def test_get_users_returns_paginated_users(self):
        response = self.client.get(
            reverse("web:users:user"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["data"]), 7)
        self.assertEqual(response_data["data"][0]["username"], "user7")
        self.assertEqual(
            response_data["meta"],
            {"currentPage": 1, "items": 9, "pages": 2, "perPage": 7},
        )

    def test_get_users_does_not_require_authentication(self):
        response = self.client.get(reverse("web:users:user"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 7)

    def test_get_users_rejects_non_integer_page(self):
        response = self.client.get(
            reverse("web:users:user"),
            {"page": "first"},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["message"],
            "The page query parameter, if provided, must be of type integer.",
        )
