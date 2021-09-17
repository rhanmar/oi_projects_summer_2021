from django.db.models import Prefetch
from django.views import generic

from ...courses.models import Comment
from .. import models


class MentorsView(generic.ListView):
    """Implement mentors page logic.

    In mentor page render all mentors which be a members of current user
    course.
    """
    template_name = "courses/mentors.html"
    context_object_name = "mentors"

    def get_queryset(self):
        """Return mentors queryset of current course."""
        current_user = self.request.user
        if current_user.courses.first():
            return self.request.user.courses.first().users.filter(
                is_staff=True
            )
        return None


class UserDetailView(generic.DetailView):
    """Implement any user page logic."""
    model = models.User
    context_object_name = "user"
    template_name = "users/profile/user.html"

    def get_queryset(self):
        """Return queryset with prefetched data."""
        return models.User.objects.all()\
            .prefetch_related("courses")\
            .prefetch_related(
            Prefetch(
                "comments",
                queryset=Comment.objects.parent_comments_in_reverse_order()
                .prefetch_related(
                    Prefetch(
                        "sub_comments",
                        queryset=Comment.objects.child_comments_in_order(),
                        to_attr="child_comments",
                    )
                ),
                to_attr="parent_comments",
            )
        )

    def get_context_data(self, **kwargs):
        """Append additional user information."""
        kwargs["user_fields"] = self.request.user.get_public_fields_dict(
            fields=(
                "email", "first_name", "last_name", "github_username"
            )
        )
        kwargs["links"] = models.UserLink.objects.filter(
            user=self.object
        )
        return super().get_context_data(**kwargs)
