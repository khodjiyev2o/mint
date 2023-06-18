from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from apps.users.api_endpoints.Login.Google.serializers import GoogleAuthSerializer

from .utils import check_google_auth, get_user_info_from_google_token


class GoogleAuth(generics.CreateAPIView):
    serializer_class = GoogleAuthSerializer

    def create(self, request, *args, **kwargs):
        google_data = GoogleAuthSerializer(data=request.data)
        if google_data.is_valid():
            token = check_google_auth(data=google_data.data)
            user_info = get_user_info_from_google_token(data=google_data.data)
            user_info["token"] = token
            return Response(
                {"success": True, "message": "Logged in successfully", "data": user_info}, status=status.HTTP_200_OK
            )
        else:
            raise AuthenticationFailed(code=403, detail="wrong google token or this google token is already expired")


__all__ = ["GoogleAuth"]
