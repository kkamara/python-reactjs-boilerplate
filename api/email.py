from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_test_email():
    email = EmailMultiAlternatives(
        subject="Test Email ✔",
        body="This is a test email.\n\nDjango App 2026.",
        from_email=settings.MAIL_FROM,
        to=settings.MAIL_TO,
    )
    email.attach_alternative(
        """
        <style>
          .lead { font-size: 18px; color: red; }
        </style>
        <div class=\"lead\">This is a test email.</div>
        <br/>
        <footer>Django App &copy; 2026.</footer>
        """,
        "text/html",
    )
    return 1 == email.send(fail_silently=True)
