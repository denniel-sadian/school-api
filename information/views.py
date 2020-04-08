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
from .permissions import IsAdminOrReadOnly


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (IsAdminOrReadOnly,)


class SectionViewSet(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (IsAdminOrReadOnly,)


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsAdminOrReadOnly,)


class GuardianViewingPermissionViewSet(ModelViewSet):
    queryset = GuardianViewingPermission.objects.all()
    serializer_class = GuardianViewingPermissionSerializer
    permission_classes = (IsAdminOrReadOnly,)


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
