from rest_framework import serializers

from grading.serializers import RecordSerializer
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
    records = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ('url', 'id', 'first_name', 'last_name', 'gender',
                  'id_number', 'cp_number', 'guardian_cp_number',
                  'address', 'photo', 'department', 'grade_level',
                  'section', 'records')


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ('url', 'id', 'name', 'students')


class SubjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('url', 'id', 'name', 'sections')


class GuardianViewingPermissionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GuardianViewingPermission
        fields = ('url', 'id', 'code', 'section', 'date')
