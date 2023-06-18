from rest_framework import serializers

from apps.preventa.models import Audio
from apps.users.models import User


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "full_name", "photo")


class PreventaAudioDetailSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer()

    class Meta:
        model = Audio
        fields = ("slug", "title", "cover", "duration_seconds", "creator")
