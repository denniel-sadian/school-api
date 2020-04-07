from django.contrib.auth.models import User
from rest_framework import serializers

from information.models import Department
from .models import Profile
from .models import ProfileUserCreationInvitation
from .models import ROLES


class UpdateAccountSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    id_number = serializers.CharField()
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    photo = serializers.ImageField()


class UserProfileSerializer(UpdateAccountSerializer):
    code = serializers.CharField(required=False)
    password = serializers.CharField()
    password1 = serializers.CharField()
    role = serializers.ChoiceField(ROLES)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }


class ProfileUserCreationInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileUserCreationInvitation
        fields = '__all__'
        extra_kwargs = {
            'code': {'write_only': True, 'required': False}
        }


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
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
