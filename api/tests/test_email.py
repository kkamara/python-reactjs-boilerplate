from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class SendEmailViewTests(TestCase):
    @patch("api.email.EmailMultiAlternatives.send", return_value=1)
    def test_send_email_returns_success(self, mocked_send):
        response = self.client.get(reverse("send_email"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Message Sent."})
        mocked_send.assert_called_once_with(fail_silently=True)

    @patch("api.email.EmailMultiAlternatives.send", return_value=0)
    def test_send_email_returns_error_when_delivery_fails(self, mocked_send):
        response = self.client.get(reverse("send_email"))

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json(),
            {"error": "Error encountered when attempting to send email."},
        )
        mocked_send.assert_called_once_with(fail_silently=True)
