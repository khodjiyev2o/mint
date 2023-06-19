from django.urls import path

from apps.preventa.api_endpoints import (
    FourReproductionPLayView,
    PreventaAudioDetailView,
)


urlpatterns = [
    path("audio/<str:slug>/", PreventaAudioDetailView.as_view(), name="preventa-audio-detail"),
    path("four-reproduction/play/<int:pk>", FourReproductionPLayView.as_view(), name="preventa-four-reproduction-play"),
]
