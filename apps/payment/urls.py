from django.urls import path

from apps.payment.api_endpoints import (
    ConfirmAPIView,
    ContentOrderCreateAPIView,
    GetLastTransactionStatusAPIView,
    TransactionHistoryListView,
)


urlpatterns = [
    path("content/", ContentOrderCreateAPIView.as_view(), name="content-order-create"),
    path("last-transaction/<int:pk>/", GetLastTransactionStatusAPIView.as_view(), name="get-last-transaction"),
    path("history/", TransactionHistoryListView.as_view(), name="transaction-history"),
    path("confirm/<int:pk>/", ConfirmAPIView.as_view(), name="confirm-transaction"),
]
