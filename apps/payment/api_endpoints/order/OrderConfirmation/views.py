from rest_framework import response, views


class ConfirmAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        print("Request is POST:", request.data)
        print("Response is POST:", request)
        return response.Response({"message": "Ok"}, status=200)

    def get(self, request, *args, **kwargs):
        print("Request is GET:", request)
        print("Request is GET:", request.query_params)
        return response.Response({"message": "Ok"}, status=200)
