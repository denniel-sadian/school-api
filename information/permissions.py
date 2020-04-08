from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission


class IsAuthenticatedOrAdmin(BasePermission):
    """
    This permission will allow viewing for authenticated users,
    but will leave the editing for the admins.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(user.is_authenticated and user.is_staff)
