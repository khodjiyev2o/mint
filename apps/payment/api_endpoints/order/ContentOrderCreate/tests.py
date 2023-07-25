from django.urls import reverse
from rest_framework.test import APITestCase

from apps.common.enums import PaymentType, Provider
from apps.payment.models import Order, UserContent, UserContentPaymentPlan
from apps.preventa.models import Audio
from apps.users.models import User


class TestContentOrderCreateView(APITestCase):
    def setUp(self):
        self.creator = User.objects.create(is_creator=True, email="samandarkhodjiyev@gmail.com")
        self.audio = Audio.objects.create(
            title="audio_title", creator=self.creator, one_month_price="500.00", four_repr_price="300.00"
        )

    def test_order_create_flow(self):
        url = reverse("content-order-create")
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.creator.tokens.get('access')}"}
        data = {
            "content": self.audio.uuid,
            "payment_type": PaymentType.ONE_MONTH,
            "provider": Provider.FLOW,
            "total_amount": self.audio.one_month_price,
        }
        response = self.client.post(url, data=data, **headers)
        assert response.status_code == 201

        assert response.json()["content"] == str(data["content"])
        assert response.json()["payment_type"] == data["payment_type"]
        assert response.json()["provider"] == data["provider"]
        assert response.json()["total_amount"] == str(data["total_amount"])
        assert response.json()["payment_url"] == {"url": "test"}

    def test_already_bought_content(self):
        new_order = Order.objects.create(
            user=self.creator,
            content=self.audio,
            payment_type=PaymentType.FOUR_TIME,
            provider=Provider.FLOW,
            total_amount=self.audio.four_repr_price,
            is_paid=True,
        )
        UserContent.objects.create(content=self.audio, user=self.creator, order=new_order)
        UserContentPaymentPlan.objects.create(
            content=self.audio,
            user=self.creator,
            order=new_order,
            payment_plan=PaymentType.FOUR_TIME,
            available_reproductions=4,
        )
        url = reverse("content-order-create")
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.creator.tokens.get('access')}"}
        data = {
            "content": self.audio.uuid,
            "payment_type": PaymentType.FOUR_TIME,
            "provider": Provider.FLOW,
            "total_amount": self.audio.four_repr_price,
        }
        response = self.client.post(url, data=data, **headers)
        assert response.status_code == 400
        assert response.json()["content"] == ["You have already bought this content"]

    def test_already_bought_content_but_expired_buy_again(self):
        new_order = Order.objects.create(
            user=self.creator,
            content=self.audio,
            payment_type=PaymentType.FOUR_TIME,
            provider=Provider.FLOW,
            total_amount=self.audio.four_repr_price,
            is_paid=True,
        )
        UserContent.objects.create(content=self.audio, user=self.creator, order=new_order)
        UserContentPaymentPlan.objects.create(
            content=self.audio,
            user=self.creator,
            order=new_order,
            payment_plan=PaymentType.FOUR_TIME,
            available_reproductions=0,
        )
        url = reverse("content-order-create")
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.creator.tokens.get('access')}"}
        data = {
            "content": self.audio.uuid,
            "payment_type": PaymentType.FOUR_TIME,
            "provider": Provider.FLOW,
            "total_amount": self.audio.four_repr_price,
        }
        response = self.client.post(url, data=data, **headers)
        assert response.status_code == 201
        assert response.json()["payment_type"] == data["payment_type"]
        assert response.json()["provider"] == data["provider"]
        assert response.json()["total_amount"] == str(data["total_amount"])
        assert response.json()["payment_url"] == {"url": "test"}
