from django.urls import path

from apps.payment.api_endpoints import ContentOrderCreateAPIView


urlpatterns = [
    path("content/", ContentOrderCreateAPIView.as_view(), name="content-order-create"),
]
