from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers

from .validators import unique_email, unique_username

USER_MODEL = get_user_model()


class RegisterUserSerializer(serializers.Serializer):
    firstName = serializers.CharField(
        max_length=19, min_length=3, required=True, trim_whitespace=True
    )
    lastName = serializers.CharField(
        max_length=19, min_length=3, required=True, trim_whitespace=True
    )
    username = serializers.CharField(
        max_length=19,
        min_length=3,
        required=True,
        trim_whitespace=True,
        validators=[
            RegexValidator(r"^[\w.@+-]+$", "Enter a valid username."),
            unique_username,
        ],
    )
    email = serializers.EmailField(
        max_length=100, required=True, trim_whitespace=True, validators=[unique_email]
    )
    password = serializers.CharField(
        write_only=True, required=True, min_length=5, max_length=19
    )
    passwordConfirmation = serializers.CharField(
        write_only=True, required=True, min_length=5, max_length=19
    )

    def validate_passwordConfirmation(self, value):
        password = self.initial_data.get("password")
        passwordConfirmation = self.initial_data.get("passwordConfirmation")
        if password != passwordConfirmation:
            raise serializers.ValidationError("Passwords do not match.")
        return value


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "date_joined",
        )
