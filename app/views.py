from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from django_ratelimit.decorators import ratelimit


def health(request):
    return JsonResponse({"message": "Success."})


catchall = ensure_csrf_cookie(
    ratelimit(
        key="ip",
        rate="40/m",
        method="GET",
    )(TemplateView.as_view(template_name="index.html"))
)
