from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Exam
from .models import Item
from .models import Choice
from .models import Session
from .models import StaffComment


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Item
        fields = ('url', 'id', 'exam', 'question', 'correct', 'choices')


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


class StaffCommentSerializer(serializers.HyperlinkedModelSerializer):
    staff = UserSerializer(read_only=True)

    class Meta:
        model = StaffComment
        fields = ('url', 'id', 'staff', 'exam', 'comment', 'date')
        extra_kwargs = {
            'date': {'read_only': True}
        }


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ('url', 'id', 'exam', 'correct', 'question', 'choices')


class ExamSerializer(serializers.HyperlinkedModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    comments = StaffCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ('url', 'id', 'teacher', 'date', 'published', 'sheets', 'items',
                  'comments')
        extra_kwargs = {
            'date': {'read_only': True},
            'teacher': {'view_name': 'user-detail', 'read_only': True},
        }


class StrippedItemSerializer(serializers.HyperlinkedModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ('url', 'id', 'exam', 'question', 'choices')


class StrippedExamSerializer(serializers.HyperlinkedModelSerializer):
    items = StrippedItemSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ('url', 'id', 'teacher', 'date', 'published', 'sheets', 'items')
