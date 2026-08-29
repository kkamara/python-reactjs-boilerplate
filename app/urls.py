from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.v1.urls")),
    path("mobile-api/v1/", include("api.mobile.v1.urls")),
    path(
        "images/<path:path>",
        serve,
        {"document_root": settings.BASE_DIR / "images"},
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r"^.*", views.catchall),
]

admin.site.site_header = "Django App"
admin.site.site_title = "Django App Admin Portal"
admin.site.index_title = "Welcome to the Django App Portal"
