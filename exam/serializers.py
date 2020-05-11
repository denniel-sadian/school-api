from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Exam
from .models import Item
from .models import Choice
from .models import Session
from .models import AdminComment


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


class AdminCommentSerializer(serializers.HyperlinkedModelSerializer):
    admin = UserSerializer(read_only=True)

    class Meta:
        model = AdminComment
        fields = ('url', 'id', 'admin', 'exam', 'comment', 'date')
        extra_kwargs = {
            'date': {'read_only': True}
        }


class ExamSerializer(serializers.HyperlinkedModelSerializer):
    comments = AdminCommentSerializer(many=True, read_only=True)

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
