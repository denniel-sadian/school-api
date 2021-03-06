from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Announcement
from .models import Department
from .models import Section
from .models import Subject
from .models import Student


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Department
        fields = ('url', 'id', 'name')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ('url', 'id', 'first_name', 'last_name', 'gender',
                  'id_number', 'cp_number', 'guardian_cp_number',
                  'address', 'photo', 'department', 'grade_level',
                  'section', 'user')


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ('url', 'id', 'name', 'students', 'department')


class SubjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Subject
        fields = ('url', 'id', 'name')


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('url', 'id', 'name', 'sections')


class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):
    staff = UserSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = ('url', 'id', 'staff', 'message', 'date')
