from django.conf import settings

from django_github_webhook.views import WebHookView

from apps.courses import models
from apps.github.constants import ALLOWED_ACTIONS
from apps.github.servises import (
    get_comment_from_github_message,
    get_jira_tag_from_branch_name,
    get_mark_from_github_message,
)
from apps.users.models import User


class WebHookReceiverView(WebHookView):
    """View for receive github requests and handle its."""

    secret = settings.GITHUB_WEBHOOK_KEY

    allowed_events = (
        "pull_request",
        "pull_request_review"
    )

    # pylint: disable=[R0914]
    # Request is required attribute for correct method work
    def pull_request(self, payload, request):
        """Create a solution from the received pull request.

        Receive pull request and create solution object with all data of this
        pull request.
        User who create PR - solution owner.
        Solution task get by a jira tag in git branch title.

        Attributes:
            payload: request body
        Return:
            dict with status
        """
        action = payload.get("action")
        if action in ALLOWED_ACTIONS:
            pull_request = payload.get("pull_request")
            user = pull_request.get("user")
            github_username = user.get("login")
            current_user = User.objects.get(
                github_username=github_username
            )
            jira_tag = get_jira_tag_from_branch_name(
                pull_request.get("head").get("label")
            )
            if not jira_tag:
                return {"status": "forked"}
            current_task = models.Task.objects.get(jira_tag=jira_tag)
            solution_from_github = models.Solution.objects.get_or_create(
                owner=current_user,
                task=current_task,
            )[0]
            solution_from_github.solution_description = pull_request.get(
                "body"
            )
            solution_from_github.save()
            return {"status": "received"}
        return {"status": "forked"}

    # pylint: disable=[R0914]
    # Request is required attribute for correct method work
    def pull_request_review(self, payload, request):
        """Create a evaluation from the received pull request review.

        Receive pull request review and create evaluation object with all data
        of this pull request review.
        Solution get by a it owner and it task.
        Task and owner get like in pull_request function.
        Evaluation owner - reviewer.

        Evaluation mark - In last Sentence in CR message reviewer need write
        mark as '...Mark 7'
        Evaluation comment - All sentences except last.

        Example of CR message:
            "It's great job. But next time will be more attentive. Mark 7"

            comment - "It's great job. But next time will be more attentive"
            mark - 7

        Attributes:
            payload: request body
        Return:
            dict with status
        """
        action = payload.get("action")
        if action != "dismissed":
            pull_request = payload.get("pull_request")
            review = payload.get("review")
            reviewer_dict = review.get("user")
            reviewer_github_username = reviewer_dict.get("login")
            reviewer = User.objects.get(
                github_username=reviewer_github_username
            )
            message = review.get("body")

            comment = get_comment_from_github_message(message)
            mark = get_mark_from_github_message(message)

            jira_tag = get_jira_tag_from_branch_name(
                pull_request.get("head").get("label")
            )
            if not jira_tag or not reviewer.is_staff:
                return {"status": "forked"}
            solution_owner_dict = pull_request.get("user")
            github_username = solution_owner_dict.get("login")
            current_task = models.Task.objects.get(jira_tag=jira_tag)
            solution_owner = User.objects.get(
                github_username=github_username
            )
            solution = models.Solution.objects.get(
                owner=solution_owner,
                task=current_task,
            )
            evaluation = models.Evaluation.objects.get_or_create(
                solution=solution,
                owner=reviewer,
            )[0]
            evaluation.comment = comment
            if mark:
                evaluation.mark = mark
            evaluation.save()
            return {"status": "received"}
        return {"status": "forked"}
