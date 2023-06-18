from rest_framework import generics

from apps.preventa.api_endpoints.audio.Detail.serializers import (
    PreventaAudioDetailSerializer,
)
from apps.preventa.models import Audio


class PreventaAudioDetailView(generics.RetrieveAPIView):
    serializer_class = PreventaAudioDetailSerializer
    queryset = Audio.objects.all()
    lookup_field = "slug"


__all__ = ["PreventaAudioDetailView"]
