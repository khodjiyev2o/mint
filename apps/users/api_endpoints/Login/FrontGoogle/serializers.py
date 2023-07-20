from rest_framework import serializers

from apps.users.models import User


class FrontGoogleAuthSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
