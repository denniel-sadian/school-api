from django.contrib.auth.models import User
from rest_framework import serializers


class UserEmployeeSerializer(serializers.Serializer):
    """
    This is the serializer that is used to create both
    user and employee objects.
    """
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    password1 = serializers.CharField()
    role = serializers.CharField()
    photo = serializers.ImageField()


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

