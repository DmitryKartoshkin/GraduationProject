from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    message = 'Пользователь не Аутентифицировался'
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """Метод проверяет, является пользователем автором или нет"""
        if obj.user == request.user:
            return True
        return False



