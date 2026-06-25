"""Database-backed blog models managed from Django admin."""

from typing import ClassVar

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.core.models import UUIDTimeStampedModel


class BlogCategory(UUIDTimeStampedModel):
    """Editorial grouping for buyer education and SEO content."""

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")
        verbose_name_plural = "blog categories"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(
                fields=("is_active", "display_order"),
                name="blogcat_active_order_idx",
            )
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogTag(UUIDTimeStampedModel):
    """Reusable labels for search, discovery, and admin organization."""

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(UUIDTimeStampedModel):
    """Published article with SEO fields and publish workflow."""

    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        PUBLISHED = "PUBLISHED", _("Published")
        ARCHIVED = "ARCHIVED", _("Archived")

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.PROTECT,
        related_name="posts",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    tags = models.ManyToManyField(BlogTag, blank=True, related_name="posts")
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.CharField(max_length=280)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="blogs/", blank=True)
    meta_title = models.CharField(max_length=180, blank=True)
    meta_description = models.CharField(max_length=280, blank=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        ordering = ("-published_at", "-created_at")
        indexes: ClassVar[list[models.Index]] = [
            models.Index(
                fields=("status", "published_at"),
                name="blogpost_status_pub_idx",
            ),
            models.Index(
                fields=("is_featured", "published_at"),
                name="blogpost_featured_pub_idx",
            ),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("blog:post-detail", kwargs={"slug": self.slug})

    @property
    def seo_title(self) -> str:
        return self.meta_title or self.title

    @property
    def seo_description(self) -> str:
        return self.meta_description or self.excerpt
