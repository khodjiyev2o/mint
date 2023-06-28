from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.payment.api_endpoints.order.TransactionHistory.serializers import (
    TransactionHistorySerializer,
)
from apps.payment.models import Transaction


class TransactionHistoryListView(ListAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(order__user=self.request.user, order__is_paid=True)


__all__ = ["TransactionHistoryListView"]
