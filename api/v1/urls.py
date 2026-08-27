from django.urls import include, path

urlpatterns = [
    path("users/", include("api.v1.users.urls")),
    path("web/", include(("api.v1.web.urls", "web"), namespace="web")),
]
