import random
import string

from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from config.celery import app
from utils.services.cache import generate_cache_key


@app.task()
def send_verification_code(email: str, cache_type: str, session: str):
    code = "".join(random.choice(string.digits) for _ in range(4))
    cache.set(generate_cache_key(cache_type, email, session), code, timeout=120)
    """ Send sms code via email """
    data = {
        "email": email,
        "code": code,
    }

    html_body = render_to_string("user_code_email.html", data)
    try:
        message = EmailMultiAlternatives(
            subject="MINT: Activation code",
            body=html_body,
            from_email="contacto@mintapp.info",
            to=[email],
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)
    except Exception as e:
        print("Error", e)
