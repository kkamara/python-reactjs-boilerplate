from django.urls import path

from .views import LoginUserAPIView, RegisterUserCreateAPIView

urlpatterns = [
    path("register/", RegisterUserCreateAPIView.as_view(), name="register_user"),
    path("login/", LoginUserAPIView.as_view(), name="login_user"),
]
