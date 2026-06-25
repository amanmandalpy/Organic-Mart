"""Admin publishing tools for OrganicMart blog content."""

from typing import ClassVar

from django.contrib import admin, messages
from django.utils import timezone
from django.utils.html import format_html

from apps.blog.models import BlogCategory, BlogPost, BlogTag


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    actions = ("publish_posts", "unpublish_posts")
    date_hierarchy = "published_at"
    filter_horizontal = ("tags",)
    list_display = (
        "title",
        "category",
        "status",
        "is_featured",
        "published_at",
        "featured_image_preview",
    )
    list_editable = ("status", "is_featured")
    list_filter = ("status", "is_featured", "category", "tags")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("title",)}
    readonly_fields = (
        "featured_image_preview",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "excerpt", "content", "meta_title")
    fieldsets = (
        ("Publishing", {"fields": ("status", "is_featured", "published_at")}),
        ("Article", {"fields": ("title", "slug", "category", "author", "tags")}),
        ("Content", {"fields": ("excerpt", "content")}),
        ("Media", {"fields": ("featured_image", "featured_image_preview")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
        ("Audit timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Image")
    def featured_image_preview(self, obj: BlogPost) -> str:
        if not obj.featured_image:
            return "-"
        return format_html(
            '<img src="{}" alt="" style="height:56px;width:84px;'
            'object-fit:cover;border-radius:8px;">',
            obj.featured_image.url,
        )

    @admin.action(description="Publish selected posts")
    def publish_posts(self, request, queryset):
        updated = queryset.update(
            status=BlogPost.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        messages.success(request, f"{updated} blog post(s) published.")

    @admin.action(description="Move selected posts to draft")
    def unpublish_posts(self, request, queryset):
        updated = queryset.update(status=BlogPost.Status.DRAFT)
        messages.success(request, f"{updated} blog post(s) moved to draft.")
