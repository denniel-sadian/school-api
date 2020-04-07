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
            there_is = ProfileUserCreationInvitation.objects.filter(code=code).exists()
            if there_is:
                p = ProfileUserCreationInvitation.objects.get(code=code)
                if p.used:
                    return False
                p.used = True
                p.save()
            return there_is
        return bool(first or second)


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user
