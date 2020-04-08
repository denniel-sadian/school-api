from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(
            request.method in SAFE_METHODS or
            user.is_authenticated and user.is_staff
        )
