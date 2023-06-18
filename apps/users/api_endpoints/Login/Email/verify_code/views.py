from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.api_endpoints.Login.Email.verify_code.serializers import (
    TokenObtainSerializer,
)
from apps.users.models import User
from utils.services.cache import CacheTypes, generate_cache_key


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer

    def post(self, request, *args, **kwargs):
        """
        "code": code from sms which you received
        "session": session key for sms code,  you must get from `send-email` api
        "email": format  as like 'samandarkhodjiyev@gmail.com'
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")
        session = serializer.validated_data.get("session")

        cache_key = generate_cache_key(CacheTypes.registration_sms_verification, email, session)

        if not self.is_code_valid(cache_key, code):
            return Response({"detail": _("Wrong code!")}, status=status.HTTP_400_BAD_REQUEST)
        user, _c = User.objects.get_or_create(email=email)
        return Response(
            {
                "success": True,
                "message": "Logged in successfully",
                "tokens": user.tokens,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def is_code_valid(cache_key, code):
        valid_code = cache.get(cache_key)
        return valid_code == code


__all__ = ["LoginView"]
