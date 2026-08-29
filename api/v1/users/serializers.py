from typing import ClassVar

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .validators import unique_email, unique_username

USER_MODEL = get_user_model()


class RegisterUserSerializer(serializers.Serializer):
    firstName = serializers.CharField(
        max_length=19,
        min_length=3,
        required=True,
        trim_whitespace=True,
        error_messages={
            "required": "The first name field is required.",
            "blank": "The first name field may not be blank.",
            "min_length": "The first name field length must be greater than 2 characters.",
            "max_length": "The first name field length must not exceed 19 characters.",
        },
    )
    lastName = serializers.CharField(
        max_length=19,
        min_length=3,
        required=True,
        trim_whitespace=True,
        error_messages={
            "required": "The last name field is required.",
            "blank": "The last name field may not be blank.",
            "min_length": "The last name field length must be greater than 2 characters.",
            "max_length": "The last name field length must not exceed 19 characters.",
        },
    )
    username = serializers.CharField(
        max_length=19,
        min_length=3,
        required=True,
        trim_whitespace=True,
        validators=[
            RegexValidator(
                r"^[\w.@+-]+$", "The username field must be a valid username."
            ),
            unique_username,
        ],
        error_messages={
            "required": "The username field is required.",
            "blank": "The username field may not be blank.",
            "min_length": "The username field length must be greater than 2 characters.",
            "max_length": "The username field length must not exceed 19 characters.",
        },
    )
    email = serializers.EmailField(
        max_length=100,
        required=True,
        trim_whitespace=True,
        validators=[unique_email],
        error_messages={
            "required": "The email field is required.",
            "blank": "The email field may not be blank.",
            "invalid": "The email field must be a valid email address.",
            "max_length": "The email field length must not exceed 100 characters.",
        },
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=5,
        max_length=19,
        error_messages={
            "required": "The password field is required.",
            "blank": "The password field may not be blank.",
            "min_length": "The password field length must be greater than 5 characters.",
            "max_length": "The password field length must not exceed 19 characters.",
        },
    )
    passwordConfirmation = serializers.CharField(
        write_only=True,
        required=True,
        min_length=5,
        max_length=19,
        error_messages={
            "required": "The password confirmation field is required.",
            "blank": "The password confirmation field may not be blank.",
            "min_length": "The password confirmation field length must be greater than 5 characters.",
            "max_length": "The password confirmation field length must not exceed 19 characters.",
        },
    )

    def validate_passwordConfirmation(self, value):
        password = self.initial_data.get("password")
        passwordConfirmation = self.initial_data.get("passwordConfirmation")
        if password != passwordConfirmation:
            raise serializers.ValidationError(
                "The password confirmation field does not match the password field."
            )
        return value

    def validate_username(self, value):
        return value.lower()


class UserResponseSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    isStaff = serializers.BooleanField(source="is_staff")
    dateJoined = serializers.DateTimeField(source="date_joined")
    avatarPath = serializers.SerializerMethodField()

    def get_avatarPath(self, user):
        avatar_name = getattr(getattr(user, "profile", None), "avatar_name", "")
        path = (
            f"{settings.MEDIA_URL}{avatar_name}"
            if avatar_name
            else "/images/profile/default-avatar.webp"
        )
        request = self.context.get("request")
        return request.build_absolute_uri(path) if request else path

    class Meta:
        model = USER_MODEL
        fields = (
            "id",
            "avatarPath",
            "username",
            "firstName",
            "lastName",
            "email",
            "isStaff",
            "dateJoined",
        )


class LoginUserSerializer(TokenObtainPairSerializer):
    default_error_messages: ClassVar[dict[str, str]] = {
        "no_active_account": "The username or password field is incorrect.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field].max_length = 255
        self.fields[self.username_field].error_messages.update(
            {
                "required": "The username field is required.",
                "blank": "The username field may not be blank.",
                "max_length": "The username field length must not exceed 255 characters.",
            }
        )
        self.fields["password"].max_length = 255
        self.fields["password"].error_messages.update(
            {
                "required": "The password field is required.",
                "blank": "The password field may not be blank.",
                "max_length": "The password field length must not exceed 255 characters.",
            }
        )


class LogoutUserSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        write_only=True,
        required=True,
        trim_whitespace=True,
        error_messages={
            "required": "The refresh field is required.",
            "blank": "The refresh field may not be blank.",
        },
    )

    def validate_refresh(self, value):
        try:
            self.token = RefreshToken(value)
        except TokenError as exc:
            raise serializers.ValidationError(
                "The refresh field must be a valid token."
            ) from exc
        return value

    def save(self, **kwargs):
        self.token.blacklist()
