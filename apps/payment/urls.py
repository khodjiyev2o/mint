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
    path("last-transaction/<int:pk>/", GetLastTransactionStatusAPIView.as_view(), name="last-transaction-status"),
    path("history/", TransactionHistoryListView.as_view(), name="transaction-history-list"),
    path("confirm/<int:pk>/", ConfirmAPIView.as_view(), name="confirm-transaction"),
    path("user/card/register/", FlowCustomerRegisterAPIView.as_view(), name="flow-cliente-register"),
    path("user/card/response/", CreditCardAddResponseView.as_view(), name="flow_credit_card_response"),
    path("user/cards/", UserCardListView.as_view(), name="user-cards-list"),
]
