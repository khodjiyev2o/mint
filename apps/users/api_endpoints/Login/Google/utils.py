from typing import Union

from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import User

from .serializers import GoogleAuthSerializer


client_id_mapping = {
    "WEB": settings.GOOGLE_CLIENT_ID,
    "IOS": settings.IOS_CLIENT_ID,
    "ANDROID": settings.ANDROID_CLIENT_ID,
}


def check_google_auth(data: GoogleAuthSerializer):
    token = verify_token(data)
    if token is not False:  # noqa
        user, _c = User.objects.get_or_create(email=token["email"], defaults={"first_name": token["name"]})  # noqa
        return user.tokens
    else:
        raise AuthenticationFailed(code=403, detail="Authentication Failed !")


def get_user_info_from_google_token(data: GoogleAuthSerializer) -> Union[dict, None]:
    token = verify_token(data)
    if token:
        return {
            "user_id": token["sub"],  # type: ignore
            "email": token["email"],  # type: ignore
            "name": token["name"],  # type: ignore
            "picture": token["picture"],  # type: ignore
        }
    return None


def verify_token(google_user: GoogleAuthSerializer) -> bool:
    CLIENT_ID = client_id_mapping.get(google_user["client"], settings.GOOGLE_CLIENT_ID)
    try:
        return id_token.verify_oauth2_token(google_user["token"], requests.Request(), CLIENT_ID)
    except ValueError:
        return False
