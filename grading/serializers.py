from rest_framework import serializers

from .models import GradingSheet
from .models import Work
from .models import Record


class RecordSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Record
        fields = '__all__'


class WorkSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Work
        fields = '__all__'


class GradingSheetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GradingSheet
        fields = ('url', 'teacher', 'subject', 'department',
                  'section', 'date', 'publish')
        extra_kwargs = {
            'date': {'read_only': True}
        }
