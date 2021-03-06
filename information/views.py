from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Announcement
from .models import Department
from .models import Section
from .models import Subject
from .models import Student
from grading.models import GradingSheetGroup
from grading.models import Card
from grading.models import ViewingPermission
from accounts.models import ProfileUserCreationPermission
from accounts.models import StudentAccountCreationPermission
from exam.models import Exam
from .serializers import DepartmentSerializer
from .serializers import SectionSerializer
from .serializers import SubjectSerializer
from .serializers import StudentSerializer
from .serializers import AnnouncementSerializer
from .permissions import IsAuthenticatedOrAdmin
from exam.permissions import IsTeacherOrAdmin


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (IsAuthenticatedOrAdmin,)


class SectionViewSet(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (IsAuthenticatedOrAdmin,)


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def perform_update(self, serializer):
        serializer.save()
        user = self.get_object().user
        if user:
            user.first_name = serializer.validated_data['first_name']
            user.last_name = serializer.validated_data['last_name']
            user.save()

    def perform_destroy(self, instance):
        if instance.user:
            instance.user.delete()
        instance.delete()


class AnnouncementViewSet(ModelViewSet):
    queryset = Announcement.objects.all().order_by('-date')
    serializer_class = AnnouncementSerializer

    def perform_create(self, serializer):
        serializer.save(staff=self.request.user)


class SummaryView(GenericAPIView):

    def get(self, request):
        data = {
            'announcements': Announcement.objects.all().count(),
            'departments': Department.objects.all().count(),
            'sections': Section.objects.all().count(),
            'subjects': Subject.objects.all().count(),
            'students': Student.objects.all().count(),
            'cards': Card.objects.all().count(),
            'sheets': GradingSheetGroup.objects.all().count(),
            'vperms': ViewingPermission.objects.all().count(),
            'regperms': ProfileUserCreationPermission.objects.all().count(),
            'studentperms': StudentAccountCreationPermission.objects.all().count(),
            'exams': Exam.objects.all().count(),
            'staff': User.objects.filter(
                Q(profile__role='admin') | Q(profile__role='teacher')
            ).count()
        }
        return Response(data, status=status.HTTP_200_OK)
