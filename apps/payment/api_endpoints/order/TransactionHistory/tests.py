from django.urls import reverse
from rest_framework.test import APITestCase

from apps.common.enums import PaymentType, Provider, TransactionStatus
from apps.payment.models import Order, Transaction
from apps.preventa.models import Audio
from apps.users.models import User


class TestTransactionHistoryView(APITestCase):
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
            payment_type=PaymentType.FOUR_TIME,
            is_paid=True,
        )
        self.transaction = Transaction.objects.create(
            order=self.order,
            transaction_id="flowOrder",
            status=TransactionStatus.PAID,
            amount=self.order.total_amount,
        )

    def test_transaction_history_view(self):
        url = reverse("transaction-history-list")
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.creator.tokens.get('access')}"}
        response = self.client.get(url, **headers)

        assert response.status_code == 200
        assert list(response.json()[0].keys()) == ["id", "order", "paid_at", "amount"]
        assert response.json()[0]["order"]["id"] == self.order.id
        assert response.json()[0]["amount"] == str(self.order.total_amount)
        assert response.json()[0]["order"]["content"]["uuid"] == str(self.order.content.uuid)
        assert response.json()[0]["order"]["content"]["title"] == self.order.content.title
