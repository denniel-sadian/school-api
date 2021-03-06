from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from information.models import Student
from information.models import Subject
from .models import GradingSheetGroup
from .models import GradingSheet
from .models import Work
from .models import Record
from .models import Card
from .models import FinalGrade
from .models import ViewingPermission
from .serializers import GradingSheetGroupSerializer
from .serializers import GradingSheetSerializer
from .serializers import VerboseGradingSheetSerializer
from .serializers import WorkSerializer
from .serializers import RecordSerializer
from .serializers import CardSerializer
from .serializers import FinalGradeSerializer
from .serializers import ViewingPermissionSerializer
from .permissions import IsTeacherAndOwnerOrReadOnly


class GradingSheetGroupView(ListCreateAPIView):
    queryset = GradingSheetGroup.objects.all()
    serializer_class = GradingSheetGroupSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
        instance = serializer.instance
        if 'mapeh' in instance.subject.name.lower():
            MAPEH = Subject.objects.filter(name__icontains='MAPEH')
            for subj in MAPEH:
                if subj.name.lower() == 'mapeh':
                    continue
                GradingSheet.objects.create(
                    group=instance,
                    teacher=self.request.user,
                    department=instance.department,
                    section=instance.section,
                    subject=subj,
                    grading=instance.grading
                )
        else:
            for grading in ['1st', '2nd', '3rd', '4th']:
                GradingSheet.objects.create(
                    group=instance,
                    teacher=self.request.user,
                    department=instance.department,
                    section=instance.section,
                    subject=instance.subject,
                    grading=grading
                )


class GSheetGroupDestroyView(DestroyAPIView):
    queryset = GradingSheetGroup.objects.all()


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
        teacher = request.user
        subject = get_object_or_404(Subject, pk=request.data['subject'])
        sheet = get_object_or_404(GradingSheet, pk=request.data['sheet'])
        grading = sheet.grading
        grades = request.data['grades']

        # Run to all of the grades
        for grade in grades:
            student = Student.objects.get(id=grade['student'])
            card = Card.objects.get_or_create(
                student=student,
                grading=grading
            )[0]
            final_grade = FinalGrade.objects.get_or_create(
                sheet=sheet,
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


class RelatedGradingSheets(GenericAPIView):

    def get(self, request, *args, **kwargs):
        sheet = get_object_or_404(GradingSheet, pk=kwargs['pk'])
        sheets = sheet.group.grading_sheets.all()
        data = VerboseGradingSheetSerializer(sheets, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class QuarterlySummary(GenericAPIView):

    def post(self, request):
        # Get the sheets
        sheets = []
        for pk in request.data['sheets']:
            sheets.append(get_object_or_404(GradingSheet, pk=pk))
        sheets.sort(key=lambda s: s.pk)
        
        # Check if sheets are published already
        for s in sheets:
            if not s.publish:
                return Response({"error": "A grading sheet is not published yet."},
                                status=status.HTTP_400_BAD_REQUEST)
        
        # Get the students
        students = sheets[0].section.students.all().order_by('last_name')

        # Build the data
        data = {'sheets': [], 'rows': []}
        for s in sheets:
            sheet = {
                'id': s.id,
                'grading': s.grading,
                'section': s.section.name,
                'subject': s.subject.name
            }
            data['sheets'].append(sheet)
        for student in students:
            row = {'grades': []}
            row['name'] = f'{student.last_name} {student.first_name}'
            row['gender'] = student.gender
            for sheet in sheets:
                grade = {
                    'col': sheets.index(sheet),
                    'subject': sheet.subject.name,
                    'grading': sheet.grading,
                    'grade': get_object_or_404(
                        FinalGrade, sheet=sheet, card__student=student).score
                }
                row['grades'].append(grade)
            data['rows'].append(row)
        
        return Response(data, status=status.HTTP_200_OK)
