from rest_framework import serializers

from .models import GradingSheet
from .models import Work
from .models import Record


class RecordSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Record
        fields = '__all__'
        extra_kwargs = {
            'date': {'read_only': True}
        }


class WorkSerializer(serializers.HyperlinkedModelSerializer):
    records = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Work
        fields = ('url', 'name', 'gsheet', 'work_type', 'highest_score', 'records',
                  'date')
        extra_kwargs = {
            'date': {'read_only': True}
        }


class GradingSheetSerializer(serializers.HyperlinkedModelSerializer):
    works = WorkSerializer(many=True, read_only=True)
    records = RecordsSerializer(many=True, read_only=True)

    class Meta:
        model = GradingSheet
        fields = ('url', 'teacher', 'subject', 'department',
                  'section', 'date', 'publish', 'works', 'records')
        extra_kwargs = {
            'date': {'read_only': True}
        }
