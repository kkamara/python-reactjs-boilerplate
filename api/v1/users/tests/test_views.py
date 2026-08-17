from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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
        self.assertEqual(response.json(), {"username": "janedoe"})
        self.assertTrue(User.objects.filter(username="janedoe").exists())
