from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import GradingSheetGroup
from .models import GradingSheet
from .models import Work
from .models import Record
from .models import Card
from .models import FinalGrade
from .models import ViewingPermission
from information.models import Department
from information.models import Section
from information.models import Subject


class RecordSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Record
        fields = ('url', 'id', 'date', 'gsheet', 'student', 'work', 'score')
        extra_kwargs = {
            'date': {'read_only': True}
        }


class WorkSerializer(serializers.HyperlinkedModelSerializer):
    records = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Work
        fields = ('url', 'id', 'name', 'gsheet', 'work_type',
                  'date', 'records', 'highest_score')
        extra_kwargs = {
            'date': {'read_only': True},
        }


class ViewingPermissionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ViewingPermission
        fields = ('url', 'id', 'section', 'code', 'date')
        extra_kwargs = {
            'date': {'read_only': True},
        }


class GradingSheetSerializer(serializers.HyperlinkedModelSerializer):
    works = WorkSerializer(many=True, read_only=True)
    records = RecordSerializer(many=True, read_only=True)
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = GradingSheet
        fields = ('url', 'id', 'teacher', 'subject', 'department',
                  'section', 'date', 'publish', 'works', 'records',
                  'grading', 'has_multiple_choice_exam',
                  'wo_percent', 'pt_percent', 'qa_percent')
        extra_kwargs = {
            'date': {'read_only': True},
            'teacher': {'read_only': True},
            'has_multiple_choice_exam': {'read_only': True}
        }


class VerboseGradingSheetSerializer(serializers.ModelSerializer):
    section = serializers.SlugRelatedField(read_only=True, slug_field='name')
    subject = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = GradingSheet
        fields = ('id', 'section', 'grading', 'subject', 'publish')


class GradingSheetGroupSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(
        queryset=Department.objects.all(), slug_field='name')
    section = serializers.SlugRelatedField(
        queryset=Section.objects.all(), slug_field='name')
    subject = serializers.SlugRelatedField(
        queryset=Subject.objects.all(), slug_field='name')
    teacher = UserSerializer(read_only=True)
    grading_sheets = VerboseGradingSheetSerializer(many=True, read_only=True)

    class Meta:
        model = GradingSheetGroup
        fields = ('id', 'department', 'section', 'subject', 'grading',
                  'grading_sheets', 'wo_percent', 'pt_percent', 'qa_percent',
                  'teacher')


class FinalGradeSerializer(serializers.HyperlinkedModelSerializer):
    subject = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = FinalGrade
        fields = ('url', 'id', 'teacher', 'score', 'subject')


class CardSerializer(serializers.HyperlinkedModelSerializer):
    final_grades = FinalGradeSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = ('url', 'id', 'grading', 'student', 'date', 'remarks',
                  'final_grades')
        depth = 2
        extra_kwargs = {
            'date': {'read_only': True},
            'grading': {'read_only': True},
            'student': {'read_only': True}
        }
