from rest_framework.permissions import BasePermission


class IsAdminOrInvited(BaseException):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)
