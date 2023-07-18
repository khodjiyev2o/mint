from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.preventa.api_endpoints.Four_reproduction_play.serializers import (
    FourReproductionPlaySerializer,
)
from apps.preventa.models import UserContentPaymentPlan


class FourReproductionPLayView(generics.UpdateAPIView):
    queryset = UserContentPaymentPlan.objects.all()
    serializer_class = FourReproductionPlaySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return UserContentPaymentPlan.objects.filter(content__slug=self.kwargs.get("slug")).last()
        except UserContentPaymentPlan.DoesNotExist:
            return UserContentPaymentPlan.objects.none()
