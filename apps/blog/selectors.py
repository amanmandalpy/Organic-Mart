"""Read-only blog queries used by templates and views."""

from django.db.models import Q, QuerySet
from django.utils import timezone

from apps.blog.models import BlogPost


def published_blog_posts() -> QuerySet[BlogPost]:
    """Return posts that are visible to customers."""
    now = timezone.now()
    return (
        BlogPost.objects.select_related("category", "author")
        .prefetch_related("tags")
        .filter(status=BlogPost.Status.PUBLISHED, category__is_active=True)
        .filter(Q(published_at__lte=now) | Q(published_at__isnull=True))
    )


def latest_blog_posts(limit: int = 3) -> QuerySet[BlogPost]:
    return published_blog_posts()[:limit]
