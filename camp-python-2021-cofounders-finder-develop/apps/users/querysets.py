from django.db.models import Count, Q, QuerySet


class CVSkillEvaluationQuerySet(QuerySet):
    """QuerySet for model CVSkillEvaluation"""

    def with_count_of_evaluations(self):
        """Get CVSkillEvaluation with count of evaluations for skills."""
        return self.annotate(
            sum_of_approved=Count(
                "evaluations",
                filter=Q(evaluated_skill__is_approved=True)
            ),
            sum_of_opposite=Count(
                "evaluations",
                filter=Q(evaluated_skill__is_approved=False)
            )
        )
