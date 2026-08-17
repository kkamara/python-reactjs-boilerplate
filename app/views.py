from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django_ratelimit.decorators import ratelimit

catchall = ensure_csrf_cookie(
    ratelimit(
        key="ip",
        rate="40/m",
        method="GET",
    )(TemplateView.as_view(template_name="index.html"))
)
