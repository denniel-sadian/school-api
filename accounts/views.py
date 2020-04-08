from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from rest_framework.generics import GenericAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status

from information.models import Department
from .serializers import UserProfileSerializer
from .serializers import ProfileSerializer
from .serializers import UserSerializer
from .serializers import LoginSerializer
from .serializers import ProfileUserCreationPermissionSerializer
from .serializers import UpdateAccountSerializer
from .serializers import PasswordSerializer
from .permissions import IsAdminOrInvited
from .models import Profile
from .models import ProfileUserCreationPermission


@api_view(['GET'])
def log_out(request):
    """
    For logging out the user.
    """
    logout(request)
    return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = IsAuthenticatedOrReadOnly


class LoginView(GenericAPIView):
    """
    View for logging user in.
    """
    serializer_class = LoginSerializer
    permission_classes = ()

    def post(self, request):
        # Do the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        
        # Authenticate and log in
        user = authenticate(username=data['username'],
                            password=data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                data = {
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
                if Profile.objects.filter(user=request.user).exists():
                    profile = ProfileSerializer(request.user.profile).data
                    data['id_number'] = profile['id_number']
                    data['role'] = profile['role']
                    data['photo'] = profile['photo']
                    data['department'] = profile['department']
                return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"},
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileView(GenericAPIView):
    """
    View for retrieving and updating user instance.
    """
    serializer_class = UpdateAccountSerializer

    def get(self, request):
        # Serialize the user
        user = UserSerializer(request.user)
        
        # Get the user's profile if it exists
        profile = None
        if Profile.objects.filter(user=request.user).exists():
            profile = ProfileSerializer(request.user.profile)
        
        # Create a profile for the user instead
        else:
            profile = Profile.objects.create(user=request.user)
            profile = ProfileSerializer(profile)
        
        data = {'user': user.data, 'profile': profile.data}
        
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Do the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        
        # Update the user
        user = request.user
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.username = data['username']
        user.email = data['email']
        user.save()
        
        # Update the profile if it exists
        if Profile.objects.filter(user=request.user).exists():
            profile = Profile.objects.get(user=user)
            profile.id_number = data['id_number']
            profile.department = Department.objects.get(id=data['department'])
            profile.photo = request.FILES['photo']
            profile.save()
        
        return Response({'message': 'Profile updated.'}, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    """
    View for changing password.
    """
    serializer_class = PasswordSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request):
        """Update the password."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        data = serializer.data
        
        auth = authenticate(username=user.username,
                            password=data['password'])
        if auth is None:
            return Response({'detail': 'Wrong password.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(data['password2'])
        user.save()
        login(request, user)
        
        return Response({'detail': 'Password has been changed.'},
                        status=status.HTTP_200_OK)


class CreateUserProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAdminOrInvited,)

    def post(self, request):
        # Do the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        
        # Do not accept if passwords will not match
        if data['password'] != data['password1']:
            return Response({'message': 'Passwords did not match.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # For the creation permission
        if 'code' in data:
            
            # Check if there's the permission
            if ProfileUserCreationPermission.objects.filter(code=data['code']).exists():
                perm = ProfileUserCreationPermission.objects.get(code=data['code'])
                
                # Don't accept if permission has been used already
                if perm.used:
                    return Response({
                        'message': 'The permission has been used already.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Override the data and mark permission as used
                else:
                    data['first_name'] = perm.first_name
                    data['last_name'] = perm.last_name
                    data['role'] = perm.role
                    data['department'] = perm.department
                    perm.used = True
                    perm.save()
        
        # Create the user based from the data
        user = User.objects.create(first_name=data['first_name'],
                                   last_name=data['last_name'],
                                   email=data['email'],
                                   username=data['username'])
        user.set_password(data['password'])
        
        # Make the user as a staff if it's an admin
        if data['role'] == 'admin':
            user.is_staff = True
        user.save()
        
        # Create the profile for the user
        Profile.objects.create(user=user,
                               id_number=data['id_number'],
                               department=data['department'],
                               role=data['role'],
                               photo=request.FILES['photo'])
        
        # Log the user in
        login(request, user)

        return Response({'message': 'Registered'}, status=status.HTTP_201_CREATED)


class AccountCreationPermissionViewSet(ModelViewSet):
    queryset = ProfileUserCreationPermission.objects.all()
    serializer_class = ProfileUserCreationPermissionSerializer
    permission_classes = (IsAdminUser,)
