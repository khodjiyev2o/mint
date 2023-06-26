from rest_framework import response, views

from apps.payment.models import Order, Transaction


class ConfirmAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs.get("pk"))
        transaction = Transaction.objects.get(order=order)
        transaction.apply()
        return response.Response({"message": "Ok"}, status=200)
