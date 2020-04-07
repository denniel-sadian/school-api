from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from .models import ProfileUserCreationInvitation


class IsAdminOrInvited(BasePermission):
    message = "You're not an admin or your code was not right."

    def has_permission(self, request, view):
        first = (
            request.method in (SAFE_METHODS + ('POST',))
        )
        second = request.user and request.user.is_staff
        if 'code' in request.data and not second:
            code = request.data['code']
            return ProfileUserCreationInvitation.objects.filter(code=code).exists()
        return bool(first or second)
