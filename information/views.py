from rest_framework.viewsets import ModelViewSet

from .models import Department
from .models import Section
from .models import Subject
from .models import GuardianViewingPermission
from .models import Student
from .serializers import DepartmentSerializer
from .serializers import SectionSerializer
from .serializers import SubjectSerializer
from .serializers import GuardianViewingPermissionSerializer
from .serializers import StudentSerializer


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class SectionViewSet(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class GuardianViewingPermissionViewSet(ModelViewSet):
    queryset = GuardianViewingPermission.objects.all()
    serializer_class = GuardianViewingPermissionSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
