from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserEmployeeSerializer


class CreateUserEmployeeView(GenericAPIView):
    serializer_class = UserEmployeeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
