from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.api_endpoints.Login.SMS.serializers import SendSMSSerializer
from utils.services.cache import CacheTypes
from utils.services.send_sms import send_verification_code_via_twillio


class SendSMSAuthenticationView(GenericAPIView):
    serializer_class = SendSMSSerializer

    @swagger_auto_schema(
        request_body=SendSMSSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        session = get_random_string(length=16)

        # check if SMS was sent to this phone  within 2 minutes for login or registration
        cache_keys = cache.keys(f"{CacheTypes.registration_sms_verification}{str(phone)}*")
        if cache_keys:
            raise ValidationError(detail={"phone": _("SMS is already sent!")}, code="timeout")

        send_verification_code_via_twillio(
            phone=str(phone), cache_type=CacheTypes.registration_sms_verification, session=session
        )
        return Response({"session": session})


__all__ = ["SendSMSAuthenticationView"]
