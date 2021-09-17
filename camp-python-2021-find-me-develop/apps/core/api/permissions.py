from rest_framework import permissions


class IsOwnerMeeting(permissions.IsAuthenticated):
    """Permission that allows edit obj only owner of the obj."""

    def has_object_permission(self, request, view, obj):
        return obj.created_by_id == request.user.id


class IsDialogMember(permissions.BasePermission):
    """Allow only dialog members to get dialogue data."""

    def has_object_permission(self, request, view, obj):
        """Check if dialog has request.user as it's member."""
        return obj.dialog_members.filter(member=request.user).exists()


class IsMessageSender(permissions.BasePermission):
    """Allow only message owner to perform unsafe requests."""

    def has_object_permission(self, request, view, obj):
        """Check if request method is safe or not.

        Returns:
            True if method is safe or user requesting unsafe method is message
                sender, otherwise False.
        """
        return obj.sender == request.user


class IsUserReviewCreator(permissions.BasePermission):
    """Allow only reviewer to change and delete review."""

    def has_object_permission(self, request, view, obj):
        """Check if request user is the reviewer."""
        return request.user.id == obj.reviewer_id


class IsBannedUser(permissions.BasePermission):
    """Permit any actions for banned user."""

    def has_permission(self, request, view):
        return not request.user.is_banned


class IsMeetingReviewOwner(permissions.BasePermission):
    """Allow only review owners perform actions on reviews."""

    def has_object_permission(self, request, view, obj):
        """Check if user and review creator are equal."""
        return obj.created_by == request.user
