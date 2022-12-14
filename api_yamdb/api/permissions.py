from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated and
                (request.user.is_superuser or request.user.role == 'admin'
                 or request.user.is_staff)
        )
