from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.payment.api_endpoints.flow.Customer.Register.serializers import (
    FlowCustomerCreateSerializer,
)
from apps.payment.models import FlowCustomer


@method_decorator(transaction.non_atomic_requests, name="dispatch")
class FlowCustomerRegisterAPIView(generics.CreateAPIView):
    queryset = FlowCustomer.objects.all()
    serializer_class = FlowCustomerCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)


__all__ = ["FlowCustomerRegisterAPIView"]
