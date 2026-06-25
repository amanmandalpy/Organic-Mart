"""Identity models created at project inception to avoid later migration pain."""

from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import UserManager
from apps.core.models import UUIDTimeStampedModel


class User(UUIDTimeStampedModel, AbstractUser):
    """Email-authenticated platform identity shared across customer/seller roles."""

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        SUSPENDED = "SUSPENDED", _("Suspended")
        DEACTIVATED = "DEACTIVATED", _("Deactivated")

    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects = UserManager()

    class Meta:
        ordering = ("-date_joined",)
        constraints = [  # noqa: RUF012 - Django model Meta options are class attrs.
            models.UniqueConstraint(
                Lower("email"),
                name="accounts_user_email_ci_uniq",
            )
        ]
        indexes = [  # noqa: RUF012 - Django model Meta options are class attrs.
            models.Index(
                fields=("status", "date_joined"),
                name="acct_user_status_joined_idx",
            )
        ]

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs) -> None:
        self.email = UserManager._normalize_email(self.email)
        super().save(*args, **kwargs)
