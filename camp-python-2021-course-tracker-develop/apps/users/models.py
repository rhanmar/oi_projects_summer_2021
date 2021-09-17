from typing import Iterable

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import CICharField
from django.db import models
from django.forms import model_to_dict
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from imagekit import models as imagekitmodels
from imagekit.processors import ResizeToFill, Transpose

from apps.core.models import BaseModel
from apps.courses.models import Comment

from . import validators as custom_validators

__all__ = (
    "User",
    "UserLink"
)

from .querysets import UserQuerySet


class UserManager(DjangoUserManager.from_queryset(UserQuerySet)):
    """Adjusted user manager that works w/o `username` field."""

    # pylint: disable=arguments-differ
    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # pylint: disable=arguments-differ
    def create_superuser(self, email, password=None, **extra_fields):
        """Create superuser instance (used by `createsuperuser` cmd)."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(
    AbstractBaseUser,
    PermissionsMixin,
    BaseModel,
):
    """Custom user model without username."""

    email = CICharField(
        verbose_name=_("Email address"),
        max_length=254,  # to be compliant with RFCs 3696 and 5321
        blank=False,
        unique=True,
        validators=[custom_validators.validate_email_domain]
    )
    first_name = models.CharField(
        verbose_name=_("First name"),
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name=_("Last name"),
        max_length=150,
        blank=True
    )
    profile_image = imagekitmodels.ProcessedImageField(
        verbose_name=_("Profile image"),
        upload_to=settings.DEFAULT_MEDIA_PATH,
        max_length=512,
        processors=[Transpose()],
        default="users/default_avatar/default.jpg",
        options={
            "quality": 100,
        },
    )
    profile_image_thumbnail = imagekitmodels.ImageSpecField(
        source="profile_image",
        processors=[
            ResizeToFill(80, 80)
        ],
    )
    bio = RichTextField(
        verbose_name=_("Bio"),
        max_length=1024,
        blank=True,
        config_name="text_only"
    )
    github_username = models.SlugField(
        max_length=39,
        default="",
        verbose_name=_("GitHub username"),
    )
    is_staff = models.BooleanField(
        verbose_name=_("Staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active."
        ),
    )
    comments = GenericRelation(Comment)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        # pylint: disable=invalid-str-returned
        return self.email

    def get_full_name(self) -> str:
        """Return full name of user if exists, otherwise email."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def get_short_name(self) -> str:
        """Return short name of user if exists, otherwise email."""
        if self.first_name:
            return self.first_name
        return self.email

    def is_mentor(self) -> bool:
        """Return True if user is in `Mentor` group, otherwise False."""
        return self.groups.filter(name="Mentor").exists()

    def get_public_fields_dict(self, fields: Iterable[str]) -> dict:
        """Retrieve passed fields `verbose_name` and values into dict.

        Args:
            fields: iterable of field names to retrieve.

        Returns:
            Dict of fields verbose names and values. If model doesn't contain
                some fields, they will be skipped.
        """
        fields_names_dict = model_to_dict(
            self,
            fields=fields
        ).keys()
        public_fields_dict = {
            self._meta.get_field(key).verbose_name: getattr(self, key)
            for key in fields_names_dict
        }
        return public_fields_dict

    def get_absolute_redirect_after_add_comment_url(self):
        """Return redirect url after added comment to this user."""
        return reverse("user", kwargs={"pk": self.id})


class UserLink(models.Model):
    """UserLink model to store any links that user want to add.

    Attributes:
        title (str): name of user's link.
        url (str): url of user's link.
        user (int): foreign key to user who obtain this link.
    """

    title = models.CharField(
        max_length=100,
        default="user link",
        verbose_name=_("Title")
    )
    url = models.URLField(
        verbose_name=_("URL")
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="links",
        verbose_name=_("User ID")
    )

    class Meta:
        ordering = ("title",)
        verbose_name = _("User link")
        verbose_name_plural = _("User links")

    def __str__(self):
        return self.title
