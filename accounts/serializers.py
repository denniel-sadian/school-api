from django.contrib.auth.models import User
from rest_framework import serializers

from information.models import Department
from .models import Profile
from .models import ProfileUserCreationPermission


class UserProfileSerializer(serializers.Serializer):
    """
    This is the serializer that is used to create both
    user and profile objects.
    """
    code = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField()
    password1 = serializers.CharField()
    role = serializers.ChoiceField(Profile.ROLES, required=False)
    gender = serializers.ChoiceField(Profile.GENDERS, required=False)
    id_number = serializers.CharField(required=False)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    photo = serializers.ImageField()


class UpdateAccountSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.ChoiceField(Profile.GENDERS)
    email = serializers.EmailField()
    id_number = serializers.CharField()
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    photo = serializers.ImageField()


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


class ProfileUserCreationPermissionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProfileUserCreationPermission
        fields = '__all__'
        extra_kwargs = {
            'used': {'read_only': True},
            'from_who': {'read_only': True}
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
