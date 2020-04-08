from rest_framework import serializers

from .models import Department
from .models import Section
from .models import Subject
from .models import GuardianViewingPermission
from .models import Student


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ('url', 'name', 'students')


class SubjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('url', 'name', 'sections')


class GuardianViewingPermissionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GuardianViewingPermission
        fields = ('url', 'code', 'section', 'date')
