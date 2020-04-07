from django.contrib.auth.models import User
from django.db.models import ImageField
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from information.models import Department
from .serializers import UserEmployeeSerializer
from .serializers import EmployeeProfileSerializer
from .serializers import LoginSerializer
from .models import Employee


class EmployeeProfileViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeProfileSerializer


class LoginView(GenericAPIView):
    """
    View for logging user in.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = authenticate(username=data['username'],
                            password=data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({
                    "token": user.auth_token.key,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"},
                            status=status.HTTP_400_BAD_REQUEST)


class CreateUserEmployeeView(GenericAPIView):
    serializer_class = UserEmployeeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = User.objects.create(first_name=data['first_name'],
                           last_name=data['last_name'],
                           email=data['email'],
                           username=data['username'],
                           password=data['password'])
        employee = Employee(user=user,
                            id_number=data['id_number'],
                            department=Department.objects.get(id=data['department']),
                            role=data['role'],
                            photo=request.FILES['photo'])
        employee.save()
        return Response(data, status=status.HTTP_201_CREATED)
