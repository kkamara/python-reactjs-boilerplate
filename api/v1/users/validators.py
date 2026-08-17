from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

USER_MODEL = get_user_model()

unique_username = UniqueValidator(queryset=USER_MODEL.objects.all(), lookup="iexact")
unique_email = UniqueValidator(queryset=USER_MODEL.objects.all(), lookup="iexact")
