from apps.courses.models import Evaluation


def evaluation(request):
    """Context engine for add to context all not marked evaluations."""
    if request.user.is_anonymous or not request.user.is_staff:
        return {}
    evaluations_without_mark = Evaluation.objects.filter(
        owner=request.user,
        mark__isnull=True,
    ).select_related("solution", )
    return {"evaluations": evaluations_without_mark}
