from django.urls import path

from apps.payment.api_endpoints import (
    ConfirmAPIView,
    ContentOrderCreateAPIView,
    CreditCardAddResponseView,
    FlowCustomerRegisterAPIView,
    GetLastTransactionStatusAPIView,
    TransactionHistoryListView,
    UserCardListView,
)


urlpatterns = [
    path("content/", ContentOrderCreateAPIView.as_view(), name="content-order-create"),
    path("last-transaction/<int:pk>/", GetLastTransactionStatusAPIView.as_view(), name="get-last-transaction"),
    path("history/", TransactionHistoryListView.as_view(), name="transaction-history"),
    path("confirm/<int:pk>/", ConfirmAPIView.as_view(), name="confirm-transaction"),
    path("flow/card/", FlowCustomerRegisterAPIView.as_view(), name="flow-cliente-register"),
    path("flow/card/response/", CreditCardAddResponseView.as_view(), name="flow_credit_card_response"),
    path("user/card/", UserCardListView.as_view(), name="user-card-list"),
]
