from rest_framework.permissions import BasePermission, SAFE_METHODS


class CustomAuthenticated(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and (obj.owner == request.user and obj.owner.is_staff == request.user.is_staff)
        )
