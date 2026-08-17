from django.urls import path

from .views import RegisterUserCreateAPIView

urlpatterns = [
    path("register/", RegisterUserCreateAPIView.as_view(), name="register-user"),
]
