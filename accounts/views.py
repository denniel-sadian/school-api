from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from information.models import Department
from .serializers import UserEmployeeSerializer
from .serializers import EmployeeSerializer
from .serializers import UserSerializer
from .serializers import LoginSerializer
from .models import Employee


@api_view(['GET'])
def log_out(request):
    """
    For logging out the user.
    """
    logout(request)
    return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    """
    View for logging user in.
    """
    serializer_class = LoginSerializer
    permission_classes = ()

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
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"},
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileView(GenericAPIView):
    """
    View for retrieving and updating user instance.
    """

    def get(self, request):
        user = UserSerializer(request.user)
        if Employee.objects.filter(user=user).exists():
            profile = EmployeeSerializer(request.user.employee)
        else:
            profile = Employee.objects.create(user=user)
            profile = EmployeeSerializer(profile)
        data = {'user': user.data, 'profile': profile.data}
        return Response(data, status=status.HTTP_200_OK)


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
