from django.contrib.auth import get_user_model
from rest_framework import generics, serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from api.utils import first_validation_error

from .serializers import (
    LoginUserSerializer,
    LogoutUserSerializer,
    RegisterUserSerializer,
    UserResponseSerializer,
)

USER_MODEL = get_user_model()


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
            username=username.lower(),
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


class LogoutUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

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
