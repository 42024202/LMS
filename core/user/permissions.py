from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    """
    Доступ:
    - Админ может всё
    - Обычный пользователь может только свои данные
    """

    def has_object_permission(self, request, view, obj):
        # Если админ → полный доступ
        if request.user.is_superuser or request.user.role == "admin":
            return True
        # Если обычный → доступ только к себе
        return obj == request.user
