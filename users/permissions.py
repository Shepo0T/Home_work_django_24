from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    message = 'Вы не относитесь к группе модераторов'
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user