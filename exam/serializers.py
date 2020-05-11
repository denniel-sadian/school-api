from rest_framework import serializers

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


class ExamSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Exam
        fields = ('url', 'id', 'teacher', 'date', 'published', 'sheets', 'items')
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


class AdminCommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AdminComment
        fields = ('url', 'id', 'admin', 'exam', 'comment', 'date')
        extra_kwargs = {
            'date': {'read_only': True}
        }


class InformativeAdminCommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AdminComment
        fields = ('url', 'id', 'admin', 'exam', 'comment', 'date')
        extra_kwargs = {
            'date': {'read_only': True},
            'admin': {'read_only': True}
        }
        depth = 1
