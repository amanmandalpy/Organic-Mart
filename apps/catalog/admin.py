"""Admin configuration for the product catalogue."""

from typing import ClassVar

from django.contrib import admin
from django.utils.html import format_html

from apps.catalog.models import Category, Product, ProductReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_featured", "display_order")
    list_editable = ("is_featured", "display_order")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "name",
        "category",
        "final_price",
        "stock",
        "status",
        "is_featured",
    )
    list_filter = ("status", "category", "is_featured")
    list_editable = ("stock", "status", "is_featured")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("name",)}
    search_fields = ("name", "sku", "seller_name")
    readonly_fields = ("image_preview", "created_at", "updated_at")
    fieldsets = (
        (
            "Catalogue",
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "short_description",
                    "description",
                    "seller_name",
                    "sku",
                    "status",
                    "is_featured",
                )
            },
        ),
        (
            "Pricing and inventory",
            {
                "fields": (
                    "price",
                    "discount_percent",
                    "stock",
                    "package_size",
                    "origin",
                )
            },
        ),
        (
            "Images and trust information",
            {
                "fields": (
                    "image",
                    "image_preview",
                    "image_emoji",
                    "image_gradient",
                    "organic_certification",
                    "benefits",
                    "ingredients",
                )
            },
        ),
        (
            "Meta",
            {"fields": ("rating_average", "rating_count", "created_at", "updated_at")},
        ),
    )

    @admin.display(description="Preview")
    def image_preview(self, obj: Product) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" alt="{}" style="height: 56px; width: 56px; '
                'object-fit: cover; border-radius: 12px;" />',
                obj.image.url,
                obj.name,
            )
        return "No image uploaded"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "reviewer_name",
        "rating",
        "is_verified_purchase",
        "is_approved",
    )
    list_filter = ("rating", "is_verified_purchase", "is_approved")
    search_fields = ("product__name", "reviewer_name", "title")
