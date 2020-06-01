from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import GradingSheet
from .models import Work
from .models import Record
from .models import Card
from .models import FinalGrade
from .models import ViewingPermission


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
                  'grading', 'sem', 'has_multiple_choice_exam',
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
        fields = ('id', 'section', 'grading', 'sem', 'subject', 'publish')


class VerboseFinalGradeSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(read_only=True, slug_field='card.student.id')
    
    class Meta:
        model = FinalGrade
        fields = ('id', 'score', 'student')


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
        fields = ('url', 'id', 'sem', 'grading', 'student', 'date', 'remarks',
                  'final_grades')
        depth = 2
        extra_kwargs = {
            'date': {'read_only': True},
            'sem': {'read_only': True},
            'grading': {'read_only': True},
            'student': {'read_only': True}
        }
