from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.api_endpoints.Login.FrontGoogle.serializers import (
    FrontGoogleAuthSerializer,
)
from apps.users.models import User


class FrontGoogleView(GenericAPIView):
    serializer_class = FrontGoogleAuthSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        user, c = User.objects.get_or_create(
            email=data["email"],
            defaults={"first_name": data["first_name"], "last_name": data["last_name"]},
        )
        return Response(
            {
                "success": True,
                "message": "Logged in successfully",
                "tokens": user.tokens,
            },
            status=status.HTTP_200_OK,
        )


__all__ = ["FrontGoogleView"]
