from django.urls import reverse
from rest_framework.test import APITestCase

from apps.common.enums import PaymentType, Provider
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
            payment_type=PaymentType.FOUR_TIME,
        )
        self.transaction = Transaction.objects.create(
            order=self.order,
            transaction_id="flowOrder",
            amount=self.order.total_amount,
        )

    def test_confirm_order_by_flow(self):
        url = reverse("confirm-transaction", kwargs={"pk": self.order.id})
        response = self.client.post(url)

        assert response.status_code == 200
        assert response.json() == {"message": "Ok"}
