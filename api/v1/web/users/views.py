from pathlib import Path
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from rest_framework import generics, serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import UserProfile
from api.utils import first_validation_error

from .serializers import (
    LoginUserSerializer,
    LogoutUserSerializer,
    RegisterUserSerializer,
    UpdateUserSerializer,
    UserResponseSerializer,
)

USER_MODEL = get_user_model()
ALLOWED_AVATAR_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_AVATAR_SIZE = 5 * 1024 * 1024


class RegisterUserCreateAPIView(generics.CreateAPIView):
    queryset = USER_MODEL.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as exc:
            return Response(
                {
                    "message": first_validation_error(exc.detail),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_user = self.perform_create(serializer)
        response_serializer = UserResponseSerializer(instance=new_user)
        headers = self.get_success_headers(response_serializer.data)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        firstName = serializer.validated_data.get("firstName")
        lastName = serializer.validated_data.get("lastName")
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        new_user = USER_MODEL.objects.create_user(
            first_name=firstName,
            last_name=lastName,
            username=username,
            email=email,
            password=password,
        )
        return new_user


class LoginUserAPIView(TokenObtainPairView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:
            raise InvalidToken(exc.args[0]) from exc
        except serializers.ValidationError as exc:
            return Response(
                {
                    "message": first_validation_error(exc.detail),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except AuthenticationFailed as exc:
            return Response(
                {
                    "message": first_validation_error(exc.detail),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = serializer.user

        response = {
            "data": {
                "user": UserResponseSerializer(instance=user).data,
                "access": serializer.validated_data.get("access"),
                "refresh": serializer.validated_data.get("refresh"),
            }
        }

        return Response(response, status=status.HTTP_200_OK)


class AuthoriseUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "user": UserResponseSerializer(instance=request.user).data,
            },
            status=status.HTTP_200_OK,
        )


class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = UpdateUserSerializer(instance=request.user, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as exc:
            return Response(
                {
                    "message": first_validation_error(exc.detail),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response({"message": "Success."}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = LogoutUserSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as exc:
            return Response(
                {
                    "message": first_validation_error(exc.detail),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response(status=status.HTTP_205_RESET_CONTENT)


class AvatarAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        avatar = request.FILES.get("avatar")
        extension = Path(avatar.name).suffix.lower() if avatar else ""
        if not avatar or extension not in ALLOWED_AVATAR_EXTENSIONS:
            return Response(
                {"message": "Please upload a JPG, JPEG, PNG, or WEBP image."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if avatar.size > MAX_AVATAR_SIZE:
            return Response(
                {"message": "The avatar image must not exceed 5 MB."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        previous_avatar_name = profile.avatar_name
        profile.avatar_name = default_storage.save(
            f"avatars/{uuid4().hex}{extension}", avatar
        )
        profile.save(update_fields=["avatar_name"])
        if previous_avatar_name:
            default_storage.delete(previous_avatar_name)

        return Response({"message": "Success."}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if profile.avatar_name:
            default_storage.delete(profile.avatar_name)
            profile.avatar_name = ""
            profile.save(update_fields=["avatar_name"])

        return Response({"message": "Success."}, status=status.HTTP_200_OK)
