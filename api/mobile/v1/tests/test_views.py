from django.test import TestCase
from django.urls import reverse


class MobileHelloViewTests(TestCase):
    def test_hello_get_returns_node_message(self):
        response = self.client.get(reverse("mobile_hello"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello from the NodeJS server."})
