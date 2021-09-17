from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.postgres.fields import CICharField
from django.core import validators
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from imagekit import models as imagekitmodels
from imagekit.processors import ResizeToFill, Transpose

from apps.core.models import BaseModel
from apps.users.constants import COUNT_OF_REPORTS
from apps.users.querysets import UserQuerySet


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

    first_name = models.CharField(
        verbose_name=_("First name"),
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        verbose_name=_("Last name"),
        max_length=30,
        blank=True
    )
    email = CICharField(
        verbose_name=_("Email address"),
        max_length=254,  # to be compliant with RFCs 3696 and 5321
        blank=False,
        unique=True,
        validators=[validators.validate_email]
    )
    bio = models.TextField(
        verbose_name=_("User information"),
        blank=True,
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
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active."
        ),
    )
    is_banned = models.BooleanField(
        verbose_name=_("Ban status"),
        default=False,
        help_text=_(
            "Designates whether the user got a lot of reports."
        ),
    )
    is_visible = models.BooleanField(
        verbose_name=_("Location status"),
        default=False,
        help_text=_(
            "Designates whether the user location is displayed on map."
        ),
    )
    location = models.OneToOneField(
        "map.Location",
        verbose_name=_("Map location"),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    avatar = imagekitmodels.ProcessedImageField(
        verbose_name=_("Avatar"),
        blank=True,
        null=True,
        upload_to=settings.DEFAULT_MEDIA_PATH,
        max_length=512,
        processors=[Transpose()],
        options={
            "quality": 100,
        },
        default="users/default_avatar/default_user_image.png",
    )
    avatar_thumbnail = imagekitmodels.ImageSpecField(
        source="avatar",
        processors=[
            ResizeToFill(50, 50)
        ],
        format="PNG",
    )

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

    def get_fullname(self):
        """Return composition of the first and the last names of the user."""
        return f"{self.first_name} {self.last_name}"

    def ban_if_reached_limit(self):
        """Update ban status if user have more than COUNT_OF_REPORTS reports"""
        if self.reports_to.count() >= COUNT_OF_REPORTS:
            self.is_banned = True
            self.save()

    def get_absolute_url(self):
        """Return user's profile url."""
        return reverse("user_profile", kwargs={"user_id": self.pk})

    @property
    def active_meetings(self):
        """Return queryset with active Meeting objs."""
        # pylint: disable=no-member
        return self.created_meetings.active_meetings()
