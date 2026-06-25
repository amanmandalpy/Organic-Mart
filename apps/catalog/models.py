"""Product catalogue models for the OrganicMart storefront."""

from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.core.models import UUIDTimeStampedModel


class Category(UUIDTimeStampedModel):
    """Organic product grouping shown on the homepage and catalogue filters."""

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=16, default="🌿")
    is_featured = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")
        verbose_name_plural = "categories"
        indexes = [  # noqa: RUF012 - Django model Meta options are class attrs.
            models.Index(
                fields=("is_featured", "display_order"),
                name="cat_featured_order_idx",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"{reverse('catalog:product-list')}?category={self.slug}#catalog-results"


class Product(UUIDTimeStampedModel):
    """Sellable organic product with customer-facing commerce details."""

    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        ACTIVE = "ACTIVE", _("Active")
        ARCHIVED = "ARCHIVED", _("Archived")

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=240)
    description = models.TextField()
    seller_name = models.CharField(max_length=140, default="OrganicMart Verified")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(90)],
    )
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=64, unique=True)
    package_size = models.CharField(max_length=80, blank=True)
    origin = models.CharField(max_length=120, blank=True)
    organic_certification = models.CharField(max_length=180)
    benefits = models.TextField(help_text="One benefit per line.")
    ingredients = models.TextField(help_text="One ingredient per line.")
    image = models.ImageField(upload_to="products/", blank=True)
    image_emoji = models.CharField(max_length=16, default="🥬")
    image_gradient = models.CharField(
        max_length=120,
        default="linear-gradient(135deg, #eef6df, #ffffff)",
    )
    rating_average = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    rating_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )

    class Meta:
        ordering = ("-is_featured", "name")
        constraints = [  # noqa: RUF012 - Django model Meta options are class attrs.
            models.CheckConstraint(
                condition=Q(price__gte=0),
                name="catalog_product_price_gte_0",
            ),
            models.CheckConstraint(
                condition=Q(stock__gte=0),
                name="catalog_product_stock_gte_0",
            ),
        ]
        indexes = [  # noqa: RUF012 - Django model Meta options are class attrs.
            models.Index(
                fields=("status", "is_featured"),
                name="prod_status_featured_idx",
            ),
            models.Index(
                fields=("category", "status"),
                name="prod_category_status_idx",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("catalog:product-detail", kwargs={"slug": self.slug})

    @property
    def final_price(self) -> Decimal:
        multiplier = Decimal(100 - self.discount_percent) / Decimal(100)
        return (self.price * multiplier).quantize(Decimal("0.01"))

    @property
    def savings(self) -> Decimal:
        return (self.price - self.final_price).quantize(Decimal("0.01"))

    @property
    def is_in_stock(self) -> bool:
        return self.stock > 0 and self.status == self.Status.ACTIVE

    @property
    def benefit_list(self) -> list[str]:
        return [line.strip() for line in self.benefits.splitlines() if line.strip()]

    @property
    def ingredient_list(self) -> list[str]:
        return [line.strip() for line in self.ingredients.splitlines() if line.strip()]

    @property
    def rating_percent(self) -> int:
        return round(float(self.rating_average) / 5 * 100)


class ProductReview(UUIDTimeStampedModel):
    """Product review model; verified-purchase enforcement comes with orders."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    reviewer_name = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=160)
    body = models.TextField()
    is_verified_purchase = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [  # noqa: RUF012 - Django model Meta options are class attrs.
            models.Index(
                fields=("product", "is_approved"),
                name="review_product_approved_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.product} - {self.rating} stars"
