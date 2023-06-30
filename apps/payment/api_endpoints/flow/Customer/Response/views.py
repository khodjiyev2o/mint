from rest_framework.response import Response
from rest_framework.views import APIView


class CreaditCardAddResponseView(APIView):
    def post(self, request, *args, **kwargs):
        print(request)
        return Response({"message": "ok"}, status=201)
