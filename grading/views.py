from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status


from information.models import Student
from information.models import Subject
from .models import GradingSheet
from .models import Work
from .models import Record
from .models import Card
from .models import FinalGrade
from .serializers import GradingSheetSerializer
from .serializers import WorkSerializer
from .serializers import RecordSerializer
from .serializers import CardSerializer
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


class CardListView(ListAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()


class WriteGradesToCardsView(GenericAPIView):

    def post(self, request):
        # Get these first
        sem = request.data['sem']
        grading = request.data['grading']
        grades = request.data['grades']
        teacher = request.user
        subject = Subject.objects.get(id=request.data['subject'])

        # Run to all of the grades
        for grade in grades:
            student = Student.objects.get(id=grade['student'])
            card = Card.objects.get_or_create(
                student=student,
                sem=sem,
                grading=grading
            )[0]
            final_grade = FinalGrade.objects.get_or_create(
                card=card,
                subject=subject,
                teacher=teacher
            )[0]
            final_grade.score = grade['score']
            final_grade.save()
        
        return Response({'detail': 'Grades have been written to their cards'},
                        status=status.HTTP_200_OK)
