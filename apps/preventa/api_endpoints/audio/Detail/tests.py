from django.urls import reverse
from rest_framework.test import APITestCase

from apps.preventa.models import Audio
from apps.users.models import User


class TestAudioDetailView(APITestCase):
    def setUp(self):
        self.creator = User.objects.create(is_creator=True, email="samandarkhodjiyev@gmail.com")
        self.audio = Audio.objects.create(title="audio_title", creator=self.creator)

    def test_audio_detail(self):
        url = reverse("preventa-audio-detail", kwargs={"slug": self.audio.slug})
        response = self.client.get(url)
        assert response.status_code == 200
        assert list(response.json().keys()) == ["slug", "title", "cover", "duration_seconds", "creator"]
        assert response.json()["slug"] == self.audio.slug
        assert response.json()["title"] == self.audio.title
        assert response.json()["cover"] == self.audio.cover
        assert response.json()["duration_seconds"] == self.audio.duration_seconds

    def test_audio_detail_invalid_slug(self):
        url = reverse("preventa-audio-detail", kwargs={"slug": "somehting_Wrong"})
        response = self.client.get(url)
        assert response.status_code == 404
        assert response.json()["detail"] == "Not found."
