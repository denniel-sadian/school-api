from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from .models import ProfileUserCreationInvitation


class IsAdminOrInvited(BasePermission):

    def has_permission(self, request, view):
        first = (
            request.method in (SAFE_METHODS + ('POST',)) or
            'code' in request.data and
            ProfileUserCreationInvitation.objects.filter(code=code).exists()
        )
        second = request.user and request.user.is_staff
        return bool(first or second)
