from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class AssociationAccount(APIView):
    def get(self, request, *args,**kwargs):
        return Response({"message":"Hello world!"}, status=status.HTTP_200_OK)