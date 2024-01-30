from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff
