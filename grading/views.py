from rest_framework.viewsets import ModelViewSet

from .models import GradingSheet
from .models import Work
from .models import Record
from .serializers import GradingSheetSerializer
from .serializers import WorkSerializer
from .serializers import RecordSerializer
from .permissions import IsTeacherAndOwnerOrReadOnly


class GradingSheetViewSet(ModelViewSet):
    serializer_class = GradingSheetSerializer
    permission_classes = (IsTeacherAndOwnerOrReadOnly,)

    def get_queryset(self):
        return GradingSheet.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class WorkViewSet(ModelViewSet):
    serializer_class = WorkSerializer
    permission_classes = (IsTeacherAndOwnerOrReadOnly,)
    
    def get_queryset(self):
        return Work.objects.filter(gsheet__teacher=self.request.user)


class RecordViewSet(ModelViewSet):
    serializer_class = RecordSerializer
    permission_classes = (IsTeacherAndOwnerOrReadOnly,)

    def get_queryset(self):
        return Record.objects.filter(gsheet__teacher=self.request.user)
