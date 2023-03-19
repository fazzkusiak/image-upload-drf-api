from rest_framework import permissions


class IsTierSuperuserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.tier.fetch_link:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if obj.image.owner == request.user:
            return True
        return False
