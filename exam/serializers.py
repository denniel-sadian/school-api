from rest_framework import serializers

from .models import Exam
from .models import Item
from .models import Choice
from .models import Session


class ExamSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Exam
        fields = ('url', 'id', 'teacher', 'date', 'sheets')
        extra_kwargs = {
            'date': {'read_only': True}
        }


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Item
        fields = ('url', 'id', 'exam', 'question', 'correct')


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Choice
        fields = ('url', 'id', 'item', 'letter', 'text')


class SessionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Session
        fields = ('url', 'id', 'student', 'exam', 'date')
        extra_kwargs = {
            'date': {'read_only': True}
        }
