from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Разрешение только для модераторов"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="moderators").exists()
        )


class IsDoctor(permissions.BasePermission):
    """Разрешение только для врача"""

    def has_object_permission(self, request, view, obj):
        return obj.doctor == request.user


class IsDoctorOrModerator(permissions.BasePermission):
    """Разрешение для врача или модератора"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        is_moderator = request.user.groups.filter(name="moderators").exists()
        is_staff = obj.doctor == request.user
        return is_moderator or is_staff


class CanCreateCourseLesson(permissions.BasePermission):
    """Модераторы НЕ могут создавать"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Модераторы не могут создавать
        if request.user.groups.filter(name="moderators").exists():
            return False
        return True
