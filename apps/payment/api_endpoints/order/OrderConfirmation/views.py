from rest_framework import response, views

from apps.payment.models import Order


class ConfirmAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        print("Confirm")
        print("args", args)
        print("kwargs", kwargs)
        print("Request is POST:", request.data)
        print("Response is POST:", request)
        order = Order.objects.get(id=self.request.kwargs.get("pk"))

        print(order)
        return response.Response({"message": "Ok"}, status=200)
