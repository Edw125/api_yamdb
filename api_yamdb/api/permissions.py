from rest_framework import permissions


class OnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.role == 'admin'


class IsAdminOrReadOnlyAnonymusPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class ReviewAndCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
        )
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return bool(
                request.user
                and request.user.is_authenticated
            )
        if request.method == 'PATCH' or request.method == 'DELETE':
            return bool(request.user.role == 'admin' or
                request.user.role == 'moderator' or
                obj.author == request.user
            )
        return False
