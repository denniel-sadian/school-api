from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserEmployeeSerializer
from .models import Employee


class CreateUserEmployeeView(GenericAPIView):
    serializer_class = UserEmployeeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = User.create(first_name=data['first_name'],
                           last_name=data['last_name'],
                           email=data['email'],
                           username=data['username'],
                           password=data['password'])
        employee = Employee.objects.create(user=user,
                                           id_number=data['id_number'],
                                           department=data['id_number'],
                                           role=data['role'],
                                           photo=data['photo'])
        return Response(data, status=status.HTTP_201_CREATED)
