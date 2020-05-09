from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsTeacherOrAdmin(BasePermission):

    def has_permission(self, request, view):
        authenticated = request.user.is_authenticated
        is_teacher_or_admin = request.user.profile.role in ['teacher', 'admin']
        return bool(authenticated and is_teacher_or_admin)
