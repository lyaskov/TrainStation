from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only requests for authenticated users,
    and write access only for admins.
    """

    def has_permission(self, request, view):
        # Разрешаем GET/HEAD/OPTIONS всем авторизованным
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # Изменения — только администраторам
        return request.user and request.user.is_staff
