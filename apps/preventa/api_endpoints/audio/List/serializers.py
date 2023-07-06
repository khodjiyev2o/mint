from rest_framework import serializers

from apps.preventa.models import Audio
from apps.users.models import User


class CreatorPreventaSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "photo")


class AudioListSerializer(serializers.ModelSerializer):
    creator = CreatorPreventaSerializer()

    class Meta:
        model = Audio
        fields = ("uuid", "slug", "cover", "title", "creator")
