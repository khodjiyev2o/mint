from django.urls import reverse
from rest_framework.test import APITestCase

from apps.payment.models import Order, PaymentType, Provider, Transaction
from apps.preventa.models import Audio
from apps.users.models import User


class TestAudioDetailView(APITestCase):
    def setUp(self):
        self.creator = User.objects.create(is_creator=True, email="samandarkhodjiyev@gmail.com")
        self.audio = Audio.objects.create(title="audio_title", creator=self.creator)

    def test_audio_detail_not_bought_content(self):
        url = reverse("preventa-audio-detail", kwargs={"slug": self.audio.slug})
        response = self.client.get(url)
        assert response.status_code == 200
        assert list(response.json().keys()) == [
            "uuid",
            "slug",
            "title",
            "cover",
            "duration_seconds",
            "creator",
            "is_bought",
            "audio_file",
            "four_repr_price",
            "price",
            "user_content_plan",
        ]
        assert response.json()["slug"] == self.audio.slug
        assert response.json()["title"] == self.audio.title
        assert response.json()["cover"] == self.audio.cover
        assert response.json()["duration_seconds"] == self.audio.duration_seconds
        assert response.json()["user_content_plan"] is None
        assert response.json()["is_bought"] is False
        assert response.json()["audio_file"] == "test_url"

    def test_audio_detail_bought_content(self):
        self.order = Order.objects.create(
            user=self.creator,
            content=self.audio,
            provider=Provider.FLOW,
            total_amount=self.audio.four_repr_price,
            is_paid=True,
            payment_type=PaymentType.FOUR_TIME,
        )
        transaction = Transaction.objects.create(
            order=self.order,
            transaction_id="flowOrder",
            amount=self.order.total_amount,
        )
        transaction.apply()
        url = reverse("preventa-audio-detail", kwargs={"slug": self.audio.slug})
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.creator.tokens.get('access')}"}
        response = self.client.get(url, **headers)
        assert response.status_code == 200
        assert list(response.json().keys()) == [
            "uuid",
            "slug",
            "title",
            "cover",
            "duration_seconds",
            "creator",
            "is_bought",
            "audio_file",
            "four_repr_price",
            "price",
            "user_content_plan",
        ]
        assert response.json()["slug"] == self.audio.slug
        assert response.json()["title"] == self.audio.title
        assert response.json()["cover"] == self.audio.cover
        assert response.json()["duration_seconds"] == self.audio.duration_seconds
        assert len(response.json()["user_content_plan"]) == 1
        assert response.json()["user_content_plan"][0]["payment_plan"] == self.order.payment_type
        assert response.json()["user_content_plan"][0]["available_reproductions"] == 4
        assert response.json()["user_content_plan"][0]["limited_reproduction"] is True
        assert response.json()["is_bought"] is True
        assert response.json()["audio_file"] == "test_url"

    def test_audio_detail_bought_content_two_times(self):
        self.order = Order.objects.create(
            user=self.creator,
            content=self.audio,
            provider=Provider.FLOW,
            total_amount=self.audio.four_repr_price,
            is_paid=True,
            payment_type=PaymentType.FOUR_TIME,
        )
        transaction = Transaction.objects.create(
            order=self.order,
            transaction_id="flowOrder",
            amount=self.order.total_amount,
        )
        transaction.apply()
        url = reverse("preventa-audio-detail", kwargs={"slug": self.audio.slug})
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.creator.tokens.get('access')}"}
        response = self.client.get(url, **headers)
        assert response.status_code == 200
        assert list(response.json().keys()) == [
            "uuid",
            "slug",
            "title",
            "cover",
            "duration_seconds",
            "creator",
            "is_bought",
            "audio_file",
            "four_repr_price",
            "price",
            "user_content_plan",
        ]
        assert response.json()["slug"] == self.audio.slug
        assert response.json()["title"] == self.audio.title
        assert response.json()["cover"] == self.audio.cover
        assert response.json()["duration_seconds"] == self.audio.duration_seconds
        assert len(response.json()["user_content_plan"]) == 1
        assert response.json()["user_content_plan"][0]["payment_plan"] == self.order.payment_type
        assert response.json()["user_content_plan"][0]["available_reproductions"] == 4
        assert response.json()["user_content_plan"][0]["limited_reproduction"] is True
        assert response.json()["is_bought"] is True
        assert response.json()["audio_file"] == "test_url"

        # user buys for one time price
        self.order = Order.objects.create(
            user=self.creator,
            content=self.audio,
            provider=Provider.FLOW,
            total_amount=self.audio.price,
            is_paid=True,
            payment_type=PaymentType.ONE_TIME,
        )
        transaction = Transaction.objects.create(
            order=self.order,
            transaction_id="flowOrder",
            amount=self.order.total_amount,
        )
        transaction.apply()
        url = reverse("preventa-audio-detail", kwargs={"slug": self.audio.slug})
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.creator.tokens.get('access')}"}
        response = self.client.get(url, **headers)
        assert response.status_code == 200
        assert response.json()["slug"] == self.audio.slug
        assert response.json()["title"] == self.audio.title
        assert response.json()["cover"] == self.audio.cover
        assert response.json()["duration_seconds"] == self.audio.duration_seconds
        assert len(response.json()["user_content_plan"]) == 1
        assert response.json()["user_content_plan"][0]["payment_plan"] == self.order.payment_type
        assert response.json()["user_content_plan"][0]["available_reproductions"] is None
        assert response.json()["user_content_plan"][0]["limited_reproduction"] is False
        assert response.json()["is_bought"] is True
        assert response.json()["audio_file"] == "test_url"

    def test_audio_detail_invalid_slug(self):
        url = reverse("preventa-audio-detail", kwargs={"slug": "somehting_Wrong"})
        response = self.client.get(url)
        assert response.status_code == 404
        assert response.json()["detail"] == "Not found."
