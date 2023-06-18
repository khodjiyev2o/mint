from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api_endpoints.Login.Email.send_code_via_email.serializers import (
    SendEmailSerializer,
)
from utils.services.cache import CacheTypes
from utils.services.send_email import send_verification_code


class SendAuthVerificationCodeView(APIView):
    @swagger_auto_schema(
        request_body=SendEmailSerializer,
        operation_description="""
            email:  as like ' samandarkhodjiyev@gmail.com '
        """,
    )
    def post(self, request, *args, **kwargs):
        serializer = SendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        session = get_random_string(length=16)

        # check if SMS was sent to this email  within 2 minutes for login or registration
        cache_keys = cache.keys(f"{CacheTypes.registration_sms_verification}{str(email)}*")
        if cache_keys:
            raise ValidationError(detail={"email": _("Email is already sent!")}, code="timeout")

        send_verification_code.delay(
            email=str(email), cache_type=CacheTypes.registration_sms_verification, session=session
        )
        return Response({"session": session})


__all__ = ["SendAuthVerificationCodeView"]
