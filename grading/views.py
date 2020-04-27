from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

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


class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = (IsTeacherAndOwnerOrReadOnly,)


class RecordViewSet(ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (IsTeacherAndOwnerOrReadOnly,)


class MultipleRecordCreateView(GenericAPIView):
    serializer_class = RecordSerializer

    def post(self, request):
        records = []
        for r in request.data['records']:
            serializer = self.get_serializer(data=r)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            records.append(serializer.data)
        return Response({'records': records}, status=status.HTTP_201_CREATED)


class WriteGradesToCards(GenericAPIView):
