"""Read-side catalogue helpers used by views and homepage sections."""

from django.db.models import QuerySet

from apps.catalog.models import Category, Product


def active_products() -> QuerySet[Product]:
    return (
        Product.objects.filter(status=Product.Status.ACTIVE)
        .select_related("category")
        .order_by("-is_featured", "name")
    )


def featured_products(limit: int = 8) -> QuerySet[Product]:
    return active_products().filter(is_featured=True)[:limit]


def featured_categories() -> QuerySet[Category]:
    return Category.objects.filter(is_featured=True).order_by("display_order", "name")
