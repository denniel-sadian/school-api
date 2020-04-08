from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from .models import Work
from .models import Record


class IsTeacherAndOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # Allow if read-only and authenticated or a teacher
        authenticated = request.user.is_authenticated
        is_teacher = authenticated and not request.user.is_staff
        if request.method in SAFE_METHODS and authenticated or is_teacher:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        # Allow authenticated users to view
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        # Allow only the owners
        if type(obj) in (Work, Record):
            return obj.gsheet.teacher == obj.teacher
        return request.user == obj.teacher
