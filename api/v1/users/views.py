from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterUserSerializer, UserResponseSerializer

USER_MODEL = get_user_model()


class RegisterUserCreateAPIView(generics.CreateAPIView):
    queryset = USER_MODEL.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
