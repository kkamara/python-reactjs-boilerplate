from django.urls import path

from .views import (
    AuthoriseUserAPIView,
    AvatarAPIView,
    LoginUserAPIView,
    RegisterUserCreateAPIView,
    UserAPIView,
)

urlpatterns = [
    path("avatar/", AvatarAPIView.as_view(), name="avatar"),
    path("register/", RegisterUserCreateAPIView.as_view(), name="register_user"),
    path("login/", LoginUserAPIView.as_view(), name="login_user"),
    path("authorise/", AuthoriseUserAPIView.as_view(), name="authorise_user"),
    path("", UserAPIView.as_view(), name="user"),
]
