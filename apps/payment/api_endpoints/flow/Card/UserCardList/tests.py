from django.urls import reverse
from rest_framework.test import APITestCase

from apps.payment.models import UserCard
from apps.users.models import User


class TestContentOrderCreateView(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="samandarkhodjiyev@gmail.com")
        self.card = UserCard.objects.create(
            user=self.user,
            type="Visa",
            last_four_digits="1234",
            registration_token="registration_token",
            confirmed=True,
        )

    def test_get_last_transaction_status(self):
        url = reverse("user-cards-list")
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.user.tokens.get('access')}"}
        response = self.client.get(url, **headers)
        assert response.status_code == 200
        assert list(response.json()[0].keys()) == ["type", "last_four_digits"]
        assert response.json()[0]["type"] == self.card.type
        assert response.json()[0]["last_four_digits"] == self.card.last_four_digits
