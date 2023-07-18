from django.urls import reverse
from rest_framework.test import APITestCase

from apps.common.enums import PaymentType, Provider
from apps.payment.models import Order, Transaction
from apps.preventa.models import Audio
from apps.users.models import User


class TestFourReproductionPlayView(APITestCase):
    def setUp(self):
        self.creator = User.objects.create(is_creator=True, email="samandarkhodjiyev@gmail.com")
        self.audio = Audio.objects.create(
            title="audio_title", creator=self.creator, price="700.00", four_repr_price="500.00"
        )
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

    def test_bought_content(self):
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
        assert response.json()["is_bought"] is True
        assert response.json()["audio_file"] == "test_url"
        assert response.json()["four_repr_price"] == str(self.audio.four_repr_price)
        assert response.json()["price"] == str(self.audio.price)
        assert response.json()["user_content_plan"][0]["payment_plan"] == self.order.payment_type
        assert response.json()["user_content_plan"][0]["available_reproductions"] == 4
        assert response.json()["user_content_plan"][0]["limited_reproduction"] is True

    def test_four_repr_decrease(self):
        url = reverse("preventa-four-reproduction-play", kwargs={"slug": self.audio.slug})
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.creator.tokens.get('access')}"}
        response = self.client.patch(url, **headers)
        assert response.json()["available_reproductions"] == 3
        assert response.json()["payment_plan"] == PaymentType.FOUR_TIME
        assert response.json()["is_bought"] is True

    def test_four_repr_decrease_to_zero(self):
        url = reverse("preventa-four-reproduction-play", kwargs={"slug": self.audio.slug})
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.creator.tokens.get('access')}"}
        response = self.client.patch(url, **headers)
        assert response.json()["available_reproductions"] == 3
        assert response.json()["payment_plan"] == PaymentType.FOUR_TIME
        assert response.json()["is_bought"] is True
        response = self.client.patch(url, **headers)
        assert response.json()["available_reproductions"] == 2
        assert response.json()["payment_plan"] == PaymentType.FOUR_TIME
        assert response.json()["is_bought"] is True
        response = self.client.patch(url, **headers)
        assert response.json()["available_reproductions"] == 1
        assert response.json()["payment_plan"] == PaymentType.FOUR_TIME
        assert response.json()["is_bought"] is True
        response = self.client.patch(url, **headers)
        assert response.json()["available_reproductions"] == 0
        assert response.json()["payment_plan"] == PaymentType.FOUR_TIME
        assert response.json()["is_bought"] is False
