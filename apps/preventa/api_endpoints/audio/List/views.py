from rest_framework.generics import ListAPIView

from apps.preventa.api_endpoints.audio.List.serializers import AudioListSerializer
from apps.preventa.models import Audio


class PreventaAudioListView(ListAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioListSerializer


__all__ = ["PreventaAudioListView"]
