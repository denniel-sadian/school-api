from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Department
from .models import Section
from .models import Subject
from .models import Student
from grading.models import GradingSheet
from grading.models import Card
from grading.models import ViewingPermission
from accounts.models import ProfileUserCreationPermission
from accounts.models import StudentAccountCreationPermission
from .serializers import DepartmentSerializer
from .serializers import SectionSerializer
from .serializers import SubjectSerializer
from .serializers import StudentSerializer
from .permissions import IsAuthenticatedOrAdmin


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


class SummaryView(GenericAPIView):

    def get(self, request):
        data = {
            'departments': Department.objects.all().count(),
            'sections': Section.objects.all().count(),
            'subjects': Subject.objects.all().count(),
            'students': Student.objects.all().count(),
            'cards': Card.objects.all().count(),
            'sheets': GradingSheet.objects.all().count(),
            'vperms': ViewingPermission.objects.all().count(),
            'regperms': ProfileUserCreationPermission.objects.all().count(),
            'studentperms': StudentAccountCreationPermission.objects.all().count
        }
        return Response(data, status=status.HTTP_200_OK)
