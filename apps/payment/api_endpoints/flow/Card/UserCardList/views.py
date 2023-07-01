from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.payment.api_endpoints.flow.Card.UserCardList.serializers import (
    UserCardListSerializer,
)
from apps.payment.models import UserCard


class UserCardListView(ListAPIView):
    serializer_class = UserCardListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserCard.objects.filter(user=self.request.user, confirmed=True)


__all__ = ["UserCardListView"]
