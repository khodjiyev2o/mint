from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.payment.api_endpoints.order.ContentOrderCreate.serializers import (
    ContentOrderCreateSerializer,
)
from apps.payment.models import Order


@method_decorator(transaction.non_atomic_requests, name="dispatch")
class ContentOrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = ContentOrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


__all__ = ["ContentOrderCreateAPIView"]
