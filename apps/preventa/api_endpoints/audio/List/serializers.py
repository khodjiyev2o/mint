from rest_framework import serializers

from apps.preventa.models import Audio
from apps.users.models import User


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "photo")


class AudioListSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer()

    class Meta:
        model = Audio
        fields = ("uuid", "slug", "cover", "title", "creator")
