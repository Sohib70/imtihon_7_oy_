from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        return obj.user == request.user