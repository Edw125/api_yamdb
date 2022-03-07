from rest_framework import permissions


class OnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.role == 'admin'


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return ((request.method in permissions.SAFE_METHODS)
                or ( request.user.is_superuser or request.user.role == 'admin'))
