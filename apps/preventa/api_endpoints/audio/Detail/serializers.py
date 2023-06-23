from rest_framework import serializers

from apps.preventa.models import Audio
from apps.users.models import User


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "full_name", "photo")


class PreventaAudioDetailSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer()
    is_bought = serializers.SerializerMethodField()
    audio_file = serializers.SerializerMethodField()

    class Meta:
        model = Audio
        fields = ("uuid", "slug", "title", "cover", "duration_seconds", "creator", "is_bought", "audio_file")

    def get_is_bought(self, obj):
        user = self.context["request"].user

        if not user.is_authenticated:
            return False

        return obj.is_bought(user)

    def get_audio_file(self, obj):
        request = self.context["request"]
        user = request.user

        if not user.is_authenticated:
            return

        if obj.is_bought(user):
            return obj.file.url

        return
