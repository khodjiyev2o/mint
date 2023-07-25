import random
import string

from django.conf import settings
from django.core.cache import cache
from twilio.rest import Client

from utils.services.cache import generate_cache_key


def send_verification_code_via_twillio(phone: str, session: str, cache_type: str):
    code = "".join(random.choice(string.digits) for _ in range(4))
    cache.set(generate_cache_key(cache_type, phone, session), code, timeout=120)

    """Send sms code via Twillio"""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body="Tu codigo es: " + code + "\n\r@web.mintapp.info #" + code, from_="+56931402162", to=phone
    )
