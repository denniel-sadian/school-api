from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission


class IsAuthenticatedOrAdmin(BasePermission):
    """
    This permission will allow viewing for authenticated users,
    but will leave the editing for the admins.
    """
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        return bool(request.user and request.user.is_staff)
