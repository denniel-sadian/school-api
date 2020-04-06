from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Employee


class UserEmployeeSerializer(serializers.Serializer):
    """
    This is the serializer that is used to create both
    user and employee objects.
    """
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    password1 = serializers.CharField()
    role = serializers.CharField()
    id_number = serializers.CharField()
    department = serializers.IntegerField()
    photo = serializers.ImageField()


class EmployeeProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    """
    Login serializer.
    """
    username = serializers.CharField()
    password = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    """
    Password serializer.
    """
    password = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        """Check if both passwords match."""
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('The passwords did not match.')
        return data

