from rest_framework import permissions


# class BlocklistPermission(permissions.BasePermission):

    # def has_permission(self, request, view):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return bool(request.user and request.user.is_authenticated)



class IsOwner(permissions.BasePermission):

    # def has_permission(self, request, view):
    #     if request.user.is_authenticated:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        """Метод проверяет является пользователем автором или нет"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user



