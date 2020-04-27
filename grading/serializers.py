from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import GradingSheet
from .models import Work
from .models import Record
from .models import Card
from .models import FinalGrade


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


class GradingSheetSerializer(serializers.HyperlinkedModelSerializer):
    works = WorkSerializer(many=True, read_only=True)
    records = RecordSerializer(many=True, read_only=True)
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = GradingSheet
        fields = ('url', 'id', 'teacher', 'subject', 'department',
                  'section', 'date', 'publish', 'works', 'records',
                  'grading', 'sem')
        extra_kwargs = {
            'date': {'read_only': True},
            'teacher': {'read_only': True}
        }


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
            'date': {'read_only': True}
        }
