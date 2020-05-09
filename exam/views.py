from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from information.models import Student
from grading.models import Record
from .models import Exam
from .models import Item
from .models import Choice
from .models import Session
from .serializers import ExamSerializer
from .serializers import ItemSerializer
from .serializers import ChoiceSerializer
from .serializers import SessionSerializer
from .permissions import IsTeacherOrAdmin


class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_class = (IsTeacherOrAdmin,)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
        for sheet in serializer.instance.sheets.all():
            sheet.works.create(work_type='e', name='Examination')
    
    def perform_destroy(self, instance):
        for sheet in instance.sheets.all():
            sheet.works.filter(work_type='e').delete()
        instance.delete()


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_class = (IsTeacherOrAdmin,)


class ChoiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_class = (IsTeacherOrAdmin,)


class SessionViewSet(ModelViewSet):
    serializer_class = SessionSerializer

    def get_queryset(self):
        return Session.objects.filter(student=self.request.user.student)


class CheckAnswers(GenericAPIView):

    def post(self, request):
        # Get the data
        student = Student.objects.get(id=request.data['student'])
        exam = Exam.objects.get(id=request.data['exam'])
        answers = request.data['answers']

        # Do not accept if answers are incomplete
        if exam.items.all().count() != len(answers):
            return Response({'detail': 'Test paper was incomplete.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Check the answers
        score = 0
        for a in answers:
            item = exam.items.get(id=a['item'])
            if a['answer'] == item.correct:
                score += 1
        
        # Create a record on the grading sheet
        gsheet = exam.sheets.get(section=student.section)
        work = sheet.works.get_or_create(work_type='e')[0]
        work.highest_score = exam.items.all().count()
        record = Record.objects.get_or_create(gsheet=gsheet, student=student, work=work)
        record.score = score
        record.save()
        
        # Create a proof of session
        Session.objects.create(exam=exam, student=student)

        # Do the results
        result = {
            'score': score,
            'out_of': exam.items.all().count()
        }

        return Response(result, status=status.HTTP_200_OK)
