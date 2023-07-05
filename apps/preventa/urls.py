from django.urls import path

from apps.preventa.api_endpoints import (
    FourReproductionPLayView,
    PreventaAudioDetailView,
    PreventaAudioListView,
)


urlpatterns = [
    path("audio/", PreventaAudioListView.as_view(), name="preventa-audio-list"),
    path("audio/<str:slug>/", PreventaAudioDetailView.as_view(), name="preventa-audio-detail"),
    path(
        "four-reproduction/play/<str:slug>", FourReproductionPLayView.as_view(), name="preventa-four-reproduction-play"
    ),
]
