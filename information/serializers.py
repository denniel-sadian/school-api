from rest_framework import serializers

from .models import Department
from .models import Section
from .models import Subject


class DepartmentSerializer(serializers.HyperLinkedModelSerializer):

    class Meta:
        model = Department
        feilds = '__all__'


class SectionSerializer(serializers.HyperLinkedModelSerializer):

    class Meta:
        model = Section
        feilds = '__all__'


class SubjectSerializer(serializers.HyperLinkedModelSerializer):

    class Meta:
        model = Subject
        feilds = '__all__'


class DepartmentSerializer(serializers.HyperLinkedModelSerializer):

    class Meta:
        model = Department
        feilds = '__all__'
