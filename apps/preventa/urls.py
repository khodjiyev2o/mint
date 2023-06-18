from django.urls import path

from apps.preventa.api_endpoints import PreventaAudioDetailView


urlpatterns = [
    path("audio/<str:slug>/", PreventaAudioDetailView.as_view(), name="preventa-audio-detail"),
]
