from django.http import JsonResponse
from django.urls import path
from django.views import View

from .email import send_test_email


class SendEmailView(View):
    def get(self, request, *args, **kwargs):
        if not send_test_email():
            return JsonResponse(
                {"error": "Error encountered when attempting to send email."},
                status=500,
            )

        return JsonResponse({"message": "Message Sent."})


urlpatterns = [
    path("", SendEmailView.as_view(), name="send_email"),
]
