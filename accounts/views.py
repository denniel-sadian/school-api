from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View
from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from information.models import Department
from information.serializers import StudentSerializer
from .serializers import UserProfileSerializer
from .serializers import ProfileSerializer
from .serializers import UserSerializer
from .serializers import LoginSerializer
from .serializers import ProfileUserCreationPermissionSerializer
from .serializers import UpdateAccountSerializer
from .serializers import PasswordSerializer
from .serializers import CodeSerializer
from .serializers import StudentAccountCreationPermissionSerializer
from .permissions import IsOwnerOrReadOnly
from .models import Profile
from .models import ProfileUserCreationPermission
from .models import StudentAccountCreationPermission
from .tokens import account_activation_token


@api_view(['GET'])
def log_out(request):
    """
    For logging out the user.
    """
    logout(request)
    return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)


class StudentAccountCreation(GenericAPIView):
    """
    View for registering a student account.
    """
    permission_classes = ()

    def post(self, request):
        # Get the permission
        perm = get_object_or_404(StudentAccountCreationPermission,
                                 code=request.data['code'])
        # Get all of the profiles that aren't yet claimed
        students = perm.section.students.filter(user=None)

        try:
            # Get the credentials from the data
            student_id = request.data['student']
            email = request.data['email']
            username = request.data['username']
            password = request.data['password']

            # Get the student
            student = students.get(id=student_id)

            # Create the user
            user = User.objects.create(
                first_name=student.first_name,
                last_name=student.last_name,
                email=email,
                username=username
            )
            user.set_password(password)

            # Make user not active and save
            user.is_active = False
            user.save()

            # Send email verification
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'sid': urlsafe_base64_encode(force_bytes(student.id)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message, html_message=message)

            return Response({'detail': 'Registered'}, status=status.HTTP_201_CREATED)

        except KeyError:
            data = StudentSerializer(students, many=True, context={'request': request}).data
            return Response(data, status=status.HTTP_200_OK)


class CheckPermissionView(GenericAPIView):
    permission_classes = ()
    serializer_class = CodeSerializer

    def post(self, request):
        # Do the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.data['code']

        # Find and give the permission
        if ProfileUserCreationPermission.objects.filter(code=code, used=False).exists():
            perm = ProfileUserCreationPermission.objects.get(code=code)
            data = ProfileUserCreationPermissionSerializer(perm).data
            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'No permission with this code.'},
                            status=status.HTTP_404_NOT_FOUND)


class UserQuery:
    """
    Queryset of users that are admins and teachers only.
    """

    def get_queryset(self):
        return User.objects.filter(
            Q(profile__role='admin') | Q(profile__role='teacher'), is_active=True
        )


class UserListView(UserQuery, ListAPIView):
    """
    List view of users.
    """
    serializer_class = UserSerializer


class UserDeleteView(UserQuery, DestroyAPIView):
    """
    Delete view of the users
    """
    permission_classes = (IsAdminUser,)
    pass


class UserDetailView(RetrieveAPIView):
    """
    Delete view of the users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
                user_data = UserSerializer(user).data
                profile_data = {}
                if Profile.objects.filter(user=request.user).exists():
                    profile_data = ProfileSerializer(request.user.profile).data
                return Response({'user': user_data, 'profile': profile_data},
                                status=status.HTTP_200_OK)
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

        try:
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
                profile.gender = data['gender']
                profile.save()
        except IntegrityError:
            return Response({'detail': 'Unique contraint.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Profile updated.'}, status=status.HTTP_200_OK)


class ChangePhotoView(APIView):
    """
    View for separately updating the photo.
    """
    parser_class = (FileUploadParser,)

    def post(self, request):
        profile = request.user.profile
        profile.photo = request.FILES['photo']
        profile.save(update_fields=['photo'])

        return Response({'detail': 'Photo has been changed.'},
                        status=status.HTTP_200_OK)


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
    permission_classes = ()

    def post(self, request):
        # Do the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        # Do not accept if passwords will not match
        if data['password'] != data['password1']:
            return Response({'detail': 'Passwords did not match.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # For the creation permission
        perm = ProfileUserCreationPermission
        if 'code' in data:

            # Check if there's the permission
            if ProfileUserCreationPermission.objects.filter(code=data['code']).exists():
                perm = ProfileUserCreationPermission.objects.get(code=data['code'])

                # Don't accept if permission has been used already
                if perm.used:
                    return Response({
                        'detail': 'The permission has been used already.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Override the data
                else:
                    data['first_name'] = perm.first_name
                    data['last_name'] = perm.last_name
                    data['gender'] = perm.gender
                    data['role'] = perm.role
                    data['department'] = perm.department
        else:
            return Response({
                        'detail': 'No permission with this code.'
                    }, status=status.HTTP_404_NOT_FOUND)

        # Create the user based from the data
        user = User.objects.create(first_name=data['first_name'],
                                   last_name=data['last_name'],
                                   email=data['email'],
                                   username=data['username'])
        user.set_password(data['password'])

        # Make the user as a staff if it's an admin
        if data['role'] == 'admin':
            user.is_staff = True

        # Make user not active and save
        user.is_active = False
        user.save()

        # Send email verification
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string('accounts/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message, html_message=message)


        # Create the profile for the user
        profile = Profile.objects.create(
            user=user,
            id_number=data['id_number'],
            gender=data['gender'],
            department=data['department'],
            role=data['role']
        )
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
            profile.save()

        # Mark the permission as used
        perm.used = True
        perm.save()

        # Log the user in
        login(request, user)

        return Response({'detail': 'Registered'}, status=status.HTTP_201_CREATED)


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            if 'sid' in request.GET:
                sid = force_text(urlsafe_base64_decode(request.GET['sid']))
                student = Student.objects.get(pk=sid)
                student.user = user
                student.save()
            return HttpResponse(f'{request.GET}')
        else:
            return HttpResponse(f'{request.GET}')


class StudentAccountPermissionViewSet(ModelViewSet):
    queryset = StudentAccountCreationPermission.objects.all()
    serializer_class = StudentAccountCreationPermissionSerializer
    permission_classes = (IsAdminUser,)


class AccountCreationPermissionViewSet(ModelViewSet):
    queryset = ProfileUserCreationPermission.objects.all()
    serializer_class = ProfileUserCreationPermissionSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(from_who=self.request.user)
