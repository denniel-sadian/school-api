from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsTeacherAndOwnerOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return False
        print('TYPE: ', type(obj))
        if not request.user.is_staff:
            return False
        return request.user == obj.teacher 
