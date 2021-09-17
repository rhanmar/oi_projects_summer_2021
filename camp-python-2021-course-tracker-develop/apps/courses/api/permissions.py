from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsMentor(BasePermission):
    """Allow access only to mentor users."""

    def has_permission(self, request, view):
        """Check if current user is a mentor."""
        return request.user.is_staff


class IsOwnerSelf(BasePermission):
    """Allow access only to user who owner of current object."""

    def has_object_permission(self, request, view, obj):
        """Check if current user a owner of object."""
        if request.method not in SAFE_METHODS:
            return obj.owner == request.user
        return True
