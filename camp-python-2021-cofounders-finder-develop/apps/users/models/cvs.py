from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.models.users import User
from apps.users.querysets import CVSkillEvaluationQuerySet


class CV(BaseModel):
    """CV model for User.

    This model is responsible for curriculum vitae of user. It contains user
    information and skills( for example: python, django etc ).

    """
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
    )
    skills = models.ManyToManyField(
        to="skills.Skill",
        through="CVSkillEvaluation"
    )
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="cvs",
    )

    def get_absolute_url(self) -> str:
        """Return absolute url to CV detail view."""
        return reverse("cv_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("CV")
        verbose_name_plural = _("CVs")


class CVSkillEvaluation(BaseModel):
    """CV skill model which store evaluation info into self.

    This model many to many link between CV and skills. Also this model store
    evaluation info link about current skill.

    """
    skill = models.ForeignKey(
        to="skills.Skill",
        on_delete=models.CASCADE,
        related_name="cv_skills",
    )
    cv_owner = models.ForeignKey(
        CV,
        on_delete=models.CASCADE,
        related_name="evaluate_skills",
    )
    evaluations = models.ManyToManyField(
        User,
        blank=True,
        through="EvaluationInfo",
    )

    objects = CVSkillEvaluationQuerySet.as_manager()

    def __str__(self) -> str:
        return self.skill.name

    class Meta:
        verbose_name = _("Current cv skill")
        verbose_name_plural = _("Current cv skills")
        unique_together = ("cv_owner", "skill")


class EvaluationInfo(BaseModel):
    """Evaluation info for user skill by another user.

    This model stores information about user evaluations of current skill of
    the another user.

    """
    is_approved = models.BooleanField(
        null=True,
        verbose_name=_("Is approved?"),
        help_text=_("This indicator shows whether the skill is approved."),
    )

    comment = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Comment"),
    )

    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="owner",
        help_text=_("User who evaluate this skill."),
    )
    skill_from_cv = models.ForeignKey(
        CVSkillEvaluation,
        on_delete=models.CASCADE,
        related_name="evaluated_skill",
        help_text=_("Skill that is being evaluated."),
    )

    def clean(self):
        self.validate_unique()
        super().clean()

    def __str__(self):
        return f"{self.owner}\'s comment"

    class Meta:
        verbose_name = _("Evaluation info")
        verbose_name_plural = _("Evaluation info")
        unique_together = ("skill_from_cv", "owner")
