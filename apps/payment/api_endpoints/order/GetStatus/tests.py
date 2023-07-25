from django.urls import reverse
from rest_framework.test import APITestCase

from apps.common.enums import PaymentType, Provider, TransactionStatus
from apps.payment.models import Order, Transaction
from apps.preventa.models import Audio
from apps.users.models import User


class TestContentOrderCreateView(APITestCase):
    def setUp(self):
        self.creator = User.objects.create(is_creator=True, email="samandarkhodjiyev@gmail.com")
        self.audio = Audio.objects.create(
            title="audio_title", creator=self.creator, one_month_price="700.00", four_repr_price="500.00"
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

    def test_get_last_transaction_status(self):
        url = reverse("last-transaction-status", kwargs={"pk": self.order.id})
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.creator.tokens.get('access')}"}
        response = self.client.get(url, **headers)
        assert response.status_code == 200
        assert list(response.json().keys()) == ["id", "status"]
        assert response.json()["status"] == TransactionStatus.PAID
