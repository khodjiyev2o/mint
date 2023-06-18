from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as djTokenObtainPairSerializer,
)


class TokenObtainSerializer(djTokenObtainPairSerializer):
    default_error_messages = {}  # type: ignore
    code = serializers.CharField()
    session = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password")

    def validate(self, attrs):
        return attrs  # don't call super().validate

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.username
        return token
