from accounts.permissions import IsOwnerOrReadOnly


class IsTeacherAndOwnerOrReadOnly(IsOwnerOrReadOnly):

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_staff)
