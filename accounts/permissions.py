from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from .models import ProfileUserCreationPermission


class IsAdminOrInvited(BasePermission):
    """
    Permission for registering users.
    """
    message = "You're not an admin or your code was not right."

    def has_permission(self, request, view):
        
        # Allow these methods
        first = (
            request.method in (SAFE_METHODS + ('POST',))
        )
        
        # Allow if the user is an admin
        second = request.user and request.user.is_staff
        
        # Allow if permitted
        if 'code' in request.data and not second:
            code = request.data['code']
            there_is = ProfileUserCreationPermission.objects.filter(code=code).exists()
            return there_is
        
        return bool(first or second)


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.from_who == request.user
