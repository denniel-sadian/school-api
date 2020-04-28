from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


from information.models import Student
from information.models import Subject
from .models import GradingSheet
from .models import Work
from .models import Record
from .models import Card
from .models import FinalGrade
from .models import ViewingPermission
from .serializers import GradingSheetSerializer
from .serializers import WorkSerializer
from .serializers import RecordSerializer
from .serializers import CardSerializer
from .serializers import FinalGradeSerializer
from .serializers import ViewingPermissionSerializer
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


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.all()


class FinalGradeViewSet(ModelViewSet):
    serializer_class = FinalGradeSerializer
    queryset = FinalGrade.objects.all()


class ViewingPermissionViewSet(ModelViewSet):
    serializer_class = ViewingPermissionSerializer
    queryset = ViewingPermission.objects.all()


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


class ViewingCardsView(GenericAPIView):
    permission_classes = ()

    def post(self, request):
        code = request.data['code']
        fname = request.data['fname']
        lname = request.data['lname']
        perm = get_object_or_404(ViewingPermission, code=code)
        cards = Card.objects.filter(
            student__section=perm.section,
            student__first_name__icontains=fname,
            student__last_name__icontains=lname
        )
        data = CardSerializer(cards, many=True, context={'request': request}).data

        return Response({'cards': data}, status=status.HTTP_200_OK)
