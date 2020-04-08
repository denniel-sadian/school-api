from rest_framework.viewsets import ModelViewSet

from .models import GradingSheet
from .models import Work
from .models import Record
from .serializers import GradingSheetSerializer
from .serializers import WorkSerializer
from .serializers import RecordSerializer
from .permissions import IsTeacherAndOwnerOrReadOnly


class GradingSheetViewSet(ModelViewSet):
    queryset = GradingSheet.objects.all()
    serializer_class = GradingSheetSerializer
    permission_classes = (IsTeacherAndOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
