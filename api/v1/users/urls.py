from django.urls import path

from .views import (
    AuthoriseUserAPIView,
    LoginUserAPIView,
    LogoutUserAPIView,
    RegisterUserCreateAPIView,
)

urlpatterns = [
    path("register/", RegisterUserCreateAPIView.as_view(), name="register_user"),
    path("login/", LoginUserAPIView.as_view(), name="login_user"),
    path("authorise/", AuthoriseUserAPIView.as_view(), name="authorise_user"),
    path("", LogoutUserAPIView.as_view(), name="logout_user"),
]
