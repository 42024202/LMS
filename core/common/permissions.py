from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsInstructorOrAdmin(BasePermission):
    """
    Студенты: только чтение
    Преподаватель: редактировать только свои объекты
    Админ/суперпользователь: полный доступ
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Все авторизованные могут читать
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        # Админ и суперюзер могут всё
        if user.is_staff or user.is_superuser:
            return True

        # Преподаватель может редактировать только свои курсы
        if getattr(user, "role", None) == "instructor":
            if hasattr(obj, "instructors"):
                return obj.instructors.filter(instructor=user).exists()

        return False


class StudentSubmission(BasePermission):
    """
    - Читать могут все авторизованные.
    - Студент может редактировать только свои Submission.
    - Инструктор/админ могут редактировать любые.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        # безопасные методы (GET, HEAD, OPTIONS) доступны всем авторизованным
        if request.method in SAFE_METHODS:
            return user.is_authenticated

        # преподаватели/админы могут редактировать любые
        if user.is_staff or user.is_superuser or getattr(user, "role", None) == "instructor":
            return True

        # студент может редактировать только свои сабмишены
        return obj.student == user

