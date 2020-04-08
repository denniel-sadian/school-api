from rest_framework import serializers

from .models import Department
from .models import Section
from .models import Subject
from .models import GuardianViewingPermission
from .models import Student


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Department
        feilds = '__all__'


class SectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Section
        feilds = '__all__'


class SubjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Subject
        feilds = '__all__'


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Department
        feilds = '__all__'


class GuardianViewingPermissionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GuardianViewingPermission
        fields = '__all__'


class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'
