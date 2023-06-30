from django.urls import path

from apps.payment.api_endpoints import (
    ConfirmAPIView,
    ContentOrderCreateAPIView,
    CreaditCardAddResponseView,
    FlowCustomerRegisterAPIView,
    GetLastTransactionStatusAPIView,
    TransactionHistoryListView,
)


urlpatterns = [
    path("content/", ContentOrderCreateAPIView.as_view(), name="content-order-create"),
    path("last-transaction/<int:pk>/", GetLastTransactionStatusAPIView.as_view(), name="get-last-transaction"),
    path("history/", TransactionHistoryListView.as_view(), name="transaction-history"),
    path("confirm/<int:pk>/", ConfirmAPIView.as_view(), name="confirm-transaction"),
    path("flow/card/", FlowCustomerRegisterAPIView.as_view(), name="flow-cliente-register"),
    path("flow/card/response/", CreaditCardAddResponseView.as_view(), name="flow_credit_card_response"),
]
