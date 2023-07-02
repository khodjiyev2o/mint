from django.urls import reverse
from rest_framework.test import APITestCase

from apps.common.enums import PaymentType, Provider
from apps.preventa.models import Audio
from apps.users.models import User


class TestContentOrderCreateView(APITestCase):
    def setUp(self):
        self.creator = User.objects.create(is_creator=True, email="samandarkhodjiyev@gmail.com")
        self.audio = Audio.objects.create(title="audio_title", creator=self.creator, price="500.00")

    def test_order_create_flow(self):
        url = reverse("content-order-create")
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.creator.tokens.get('access')}"}
        data = {
            "content": self.audio.uuid,
            "payment_type": PaymentType.ONE_TIME,
            "provider": Provider.FLOW,
            "total_amount": self.audio.price,
        }
        response = self.client.post(url, data=data, **headers)

        assert response.status_code == 201

        assert response.json()["content"] == str(data["content"])
        assert response.json()["payment_type"] == data["payment_type"]
        assert response.json()["provider"] == data["provider"]
        assert response.json()["total_amount"] == str(data["total_amount"])
        assert response.json()["payment_url"] == {"url": "test"}
